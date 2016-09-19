#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
测试多个用户编写同一个清单
"""
from selenium import webdriver
from .base import FunctionalTest
from .home_and_list_pages import HomePage
import unittest

__author__ = '__L1n__w@tch'


def quit_if_possible(browser):
    try:
        browser.quit()
    except:
        pass


class SharingTest(FunctionalTest):
    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        # Y 是已登录用户
        self.create_pre_authenticated_session("edith@example.com")
        edith_browser = self.browser
        self.addCleanup(lambda: quit_if_possible(edith_browser))

        # 她的朋友 Oniciferous 也在使用这个清单网站
        oni_browser = webdriver.Firefox()
        self.addCleanup(lambda: quit_if_possible(oni_browser))
        self.browser = oni_browser
        self.create_pre_authenticated_session("oniciferous@example.com")

        # Y 访问首页，新建一个清单
        self.browser = edith_browser
        # self.browser.get(self.server_url)
        # 与网站交互
        list_page = HomePage(self).start_new_list("Get help")

        # 她看到”分享这个清单“选项
        share_box = list_page.get_share_box()
        self.assertEqual(
            share_box.get_attribute("placeholder"),
            "your-friend@example.com"
        )

        # 她分享自己的清单之后，页面更新了
        # 提示已经分享给 Oniciferous
        list_page.share_list_with("oniciferous@example.com")

        # 现在 Oniciferous 在他的浏览器中访问清单页面
        self.browser = oni_browser
        HomePage(self).go_to_home_page().go_to_my_lists_page()

        # 他看到了 Y 分享的清单
        self.browser.find_element_by_link_text("Get help").click()

        # 她看到“分享这个清单”选项
        # 猜想页面更新后的状态
        # self.wait_for(
        #     lambda: self.assertEqual(
        #         self.browser.find_element_by_css_selector(
        #             "input[name=email]"
        #         ).get_attribute("placeholder"),
        #         "your-friend@example.com"
        #     )
        # )
        # share_box = self.browser.find_element_by_css_selector("input[name=email]")
        # self.assertEqual(share_box.get_attribute("placeholder"), "your-friend@example.com")
        # self.browser = edith_browser
        pass


if __name__ == "__main__":
    pass
