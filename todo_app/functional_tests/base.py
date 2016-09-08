#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 各个功能测试的基类
"""
import sys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from server_tools import reset_database

__author__ = '__L1n__w@tch'


class FunctionalTest(StaticLiveServerTestCase):
    # setUpClass 方法和 setUp 类似，也由 unittest 提供，但是它用于设定整个类的测试背景。
    # 也就是说，setUpClass 方法只会执行一次，而不会在每个测试方法运行前都执行。
    # LiveServerTestCase 和 StaticLiveServerCase 一般都在这个方法中启动测试服务器。
    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:  # 在命令行中查找参数 liveserver(从 sys.argv 中获取)
            if "liveserver" in arg:
                # 如果找到了，就让测试类跳过常规的 setUpClass 方法，把过渡服务器的 URL 赋值给 server_url 变量
                cls.server_host = arg.split("=")[1]
                # 如果检测到命令行参数中有 liveserver, 就不仅存储 cls.server_url 属性，还存储 server_host 和 against_staging 属性
                cls.server_url = "http://" + cls.server_host
                cls.against_staging = True
                return
        super().setUpClass()
        cls.against_staging = False
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if not cls.against_staging:
            super().tearDownClass()

    # @classmethod
    # def tearDownClass(cls):
    #     if cls.server_url == cls.live_server_url:
    #         super().tearDownClass()

    def setUp(self):
        """
        setUp 是特殊的方法, 在各个测试方法之前运行。
        使用这个方法打开浏览器。
        :return:
        """
        # 需要在两次测试之间还原服务器中数据库的方法
        if self.against_staging:
            reset_database(self.server_host)
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)  # 等待 3 秒钟

    def tearDown(self):
        """
        tearDown 是特殊的方法, 在各个测试方法之后运行。使用这个方法关闭浏览器.
        注意, 这个方法有点类似 try/except 语句, 就算测试中出错了, 也会运行 tearDown 方法(如果 setUp 出错了就不会执行这个方法).
        所以测试结束后, Firefox 窗口不会一直停留在桌面上了.
        :return:
        """
        # 她很满意, 去睡觉了
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        """
        测试给定字符串是否在表格中
        :param row_text: 需要判断的字符串
        :return: None
        """
        table = self.browser.find_element_by_id("id_list_table")
        rows = table.find_elements_by_tag_name("tr")
        # self.assertTrue(
        #     any(row.text == row_text for row in rows),
        #     "New to-do item did not appear in table -- its text was:\n{}".format(table.text)
        # )
        self.assertIn(row_text, [row.text for row in rows])  # 这句话与上面那句等价, 不过精简了很多

    def get_item_input_box(self):
        return self.browser.find_element_by_id("id_text")

    def wait_for_element_with_id(self, element_id):
        WebDriverWait(self.browser, timeout=30).until(
            lambda b: b.find_element_by_id(element_id), "Could not find element with id {}. Page text was {}"
                .format(element_id, self.browser.find_element_by_tag_name("body").text))

    def wait_to_be_logged_in(self, email):
        self.wait_for_element_with_id("id_logout")
        navbar = self.browser.find_element_by_css_selector(".navbar")
        self.assertIn(email, navbar.text)

    def wait_to_be_logged_out(self, email):
        self.wait_for_element_with_id("id_login")
        navbar = self.browser.find_element_by_css_selector(".navbar")
        self.assertNotIn(email, navbar.text)


if __name__ == "__main__":
    pass
