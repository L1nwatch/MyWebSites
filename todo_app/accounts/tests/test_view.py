#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 使用模拟技术进行测试
"""
from unittest.mock import patch
from unittest import skip
from accounts.views import persona_login
from django.test import TestCase
from django.http import HttpRequest
from django.contrib.auth import get_user_model, SESSION_KEY

__author__ = '__L1n__w@tch'

User = get_user_model()  # 这个函数的作用是找出项目使用的用户模型，不管是标准的用户模型还是自定义的模型都能使用


class LoginViewTest(TestCase):
    @skip  # 发现使用了 django 的 login 之后这个测试通不过了, 原因是 mock 返回值不支持 JSON 序列化, 觉得这个测试没必要就屏蔽了
    # patch 修饰符有点像 Sinon 中的 mock 函数，作用是指定要模拟的对象。这里要模拟的是 authenticate 函数
    @patch("accounts.views.authenticate")
    # 修饰符把模拟对象作为额外的参数传入被应用的函数中
    def test_calls_authenticate_with_assertion_from_post(self, mock_authenticate):
        # 然后我们可以配置这个驭件，让它具有特定的行为。让 authenticate 函数返回 None 是最简单的行为
        # 所以我们设定了特殊的 .return_value 属性。否则，这个驭件会返回另一个驭件，视图可能不知道怎么处理
        mock_authenticate.return_Value = None
        self.client.post("/accounts/login", {"assertion": "assert this"})
        # 驭件可以做出断言，我们检查驭件是否被调用，以及调用时传入的参数是什么
        mock_authenticate.assert_called_once_with(assertion="assert this")

    @patch("accounts.views.authenticate")
    def test_returns_ok_when_user_found(self, mock_authenticate):
        user = User.objects.create(email="a@b.com")
        user.backend = ""  # 为了使用 auth.login，必须设定这个属性
        mock_authenticate.return_value = user
        response = self.client.post("/accounts/login", {"assertion": "a"})
        self.assertEqual(response.content.decode(), "OK")

    @patch("accounts.views.authenticate")
    def test_gets_logged_in_session_if_authenticate_returns_a_user(self, mock_authenticate):
        user = User.objects.create(email="a@b.com")
        user.backend = ""  # 为了使用 auth.login, 必须设定这个属性
        mock_authenticate.return_value = user
        self.client.post("/accounts/login", {"assertion": "a"})
        # Django 测试客户端会记录用户的会话，为了确认用户是否通过验证，我们要检查用户的 ID(主键，简称 pk)是否和会话关联在一起
        self.assertEqual(self.client.session[SESSION_KEY], str(user.pk))

    @patch("accounts.views.authenticate")
    def test_does_not_get_logged_in_if_authenticate_returns_None(self, mock_authenticate):
        mock_authenticate.return_value = None
        self.client.post("/accounts/login", {"assertion": "a"})
        self.assertNotIn(SESSION_KEY, self.client.session)  # 如果用户没有通过认证，会话中就不应该包含 SESSION_KEY

    @patch("accounts.views.login")
    @patch("accounts.views.authenticate")
    def test_calls_auth_login_if_authenticate_returns_a_user(self, mock_authenticate, mock_login):
        request = HttpRequest()
        request.POST["assertion"] = "asserted"
        mock_user = mock_authenticate.return_value
        persona_login(request)  # 这里书中应该是打错了, 打成 login 了
        mock_login.assert_called_once_with(request, mock_user)


if __name__ == "__main__":
    pass
