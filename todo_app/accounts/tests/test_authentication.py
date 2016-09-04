#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 为自定义认证写测试
"""
from unittest.mock import patch
from django.test import TestCase
from accounts.authentication import (
    PERSONA_VERIFY_URL, DOMAIN, PersonaAuthenticationBackend
)
from django.contrib.auth import get_user_model

User = get_user_model()

__author__ = '__L1n__w@tch'


@patch("accounts.authentication.requests.post")  # patch 修饰器也可以在类上使用，这样，类中的每个测试方法都会应用这个修饰器，而且驭件会传入每个测试方法
class AuthenticateTest(TestCase):
    def setUp(self):
        self.backend = PersonaAuthenticationBackend()  # 现在我们可以在 setUp 函数中准备所有测试都会用到的变量
        user = User(email="other@user.com")
        # 在默认情况下，Django 的用户都有 username 属性，其值必须具有唯一性。
        # 这里使用的值只是一个占位符，方便我们创建多个用户。后面我们要使用电子邮件做主键，到时候就不用用户名了。
        user.username = "other_user"
        user.save()

    def test_sends_assertion_to_mozilla_with_domain(self, mock_post):
        self.backend.authenticate("an assertion")
        mock_post.assert_called_once_with(
            PERSONA_VERIFY_URL,
            data={"assertion": "an assertion", "audience": DOMAIN}
        )

    def test_returns_none_if_response_errors(self, mock_post):
        # 现在每个测试只调整需要设定的变量，而没有设定一堆重复的样板代码，所以测试更具易读性
        mock_post.return_value.ok = False
        mock_post.return_value.json.return_value = {}
        user = self.backend.authenticate("an assertion")
        self.assertIsNone(user)

    def test_returns_none_if_status_not_okay(self, mock_post):
        # 现在每个测试只调整需要设定的变量，而没有设定一堆重复的样板代码，所以测试更具易读性
        mock_post.return_value.json.return_value = {
            "status": "not okay!"}
        user = self.backend.authenticate("an assertion")
        self.assertIsNone(user)

    def test_finds_existing_user_with_email(self, mock_post):
        mock_post.return_value.json.return_value = {"status": "okay", "email": "a@b.com"}
        actual_user = User.objects.create(email="a@b.com")
        found_user = self.backend.authenticate("an assertion")
        self.assertEqual(found_user, actual_user)

    def test_creates_new_user_if_necessary_for_valid_assertion(self, mock_post):
        mock_post.return_value.json.return_value = {"status": "okay", "email": "a@b.com"}
        found_user = self.backend.authenticate("an assertion")
        new_user = User.objects.get(email="a@b.com")
        self.assertEqual(found_user, new_user)


class GetUserTest(TestCase):
    def test_gets_user_by_email(self):
        backend = PersonaAuthenticationBackend()
        other_user = User(email="other@user.com")
        other_user.username = "other_user"
        other_user.save()
        desired_user = User.objects.create(email="a@b.com")
        found_user = backend.get_user("a@b.com")
        self.assertEqual(found_user, desired_user)

    def test_returns_none_if_no_user_with_that_email(self):
        backend = PersonaAuthenticationBackend()
        self.assertIsNone(
            backend.get_user("a@b.com")
        )


# 重构之前的测试代码
# class AuthenticateTest(TestCase):
#     @patch("accounts.authentication.requests.post")
#     def test_sends_assertion_to_mozilla_with_domain(self, mock_post):
#         backend = PersonaAuthenticationBackend()
#         backend.authenticate("an assertion")
#         mock_post.assert_called_once_with(
#             PERSONA_VERIFY_URL,
#             data={"assertion": "an assertion", "audience": DOMAIN}
#         )
#
#     @patch("accounts.authentication.requests.post")
#     def test_returns_none_if_response_errors(self, mock_post):
#         mock_post.return_value.ok = False
#         backend = PersonaAuthenticationBackend()
#
#         user = backend.authenticate("an assertion")
#         self.assertIsNone(user)


if __name__ == "__main__":
    pass
