#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
跳过认证, 进行功能测试
"""
from unittest import skip
from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
from django.contrib.sessions.backends.db import SessionStore
from base import FunctionalTest

__author__ = '__L1n__w@tch'

User = get_user_model()


class MyListsTest(FunctionalTest):
    @skip("这个只能在本地绕过认证, 远程功能测试时使用不了")
    def create_pre_authenticated_session(self, email):
        user = User.objects.create(email=email)
        session = SessionStore()
        # 在数据库中创建一个会话对象。会话键的值是用户对象的主键，即用户的电子邮件地址
        session[SESSION_KEY] = user.pk
        session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
        session.save()

        ## 为了设定 cookie，我们要先访问网站
        ## 而 404 页面是加载最快的
        self.browser.get(self.server_url + "/404_no_such_url/")
        # 然后把一个 cookie 添加到浏览器中，cookie 的值和服务器中的会话匹配。这样再次访问网站时，服务器就能识别已登录的用户。
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session.session_key,
            path="/",
        ))

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        email = "edith@example.com"

        self.browser.get(self.server_url)
        self.wait_to_be_logged_out(email)

        # Y 是已登录用户
        self.create_pre_authenticated_session(email)

        self.browser.get(self.server_url)
        self.wait_to_be_logged_in(email)


if __name__ == "__main__":
    pass
