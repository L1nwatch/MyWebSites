#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
跳过认证, 进行功能测试
"""
from unittest import skip
from server_tools import create_session_on_server
from base import FunctionalTest
from management.commands.create_session import create_pre_authenticated_session

from django.conf import settings
from django.contrib.auth import get_user_model

__author__ = '__L1n__w@tch'

User = get_user_model()


class MyListsTest(FunctionalTest):
    def create_pre_authenticated_session(self, email):
        if self.against_staging:
            session_key = create_session_on_server(self.server_host, email)
        else:
            session_key = create_pre_authenticated_session(email)
        ## 为了设定 cookie，我们要先访问网站
        ## 而 404 页面是加载最快的
        self.browser.get(self.server_url + "/404_no_such_url/")
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session_key,
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
