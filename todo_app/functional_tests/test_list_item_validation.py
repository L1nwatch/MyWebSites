#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
针对用户输入的合法性进行测试
"""
from unittest import skip
from base import FunctionalTest

__author__ = '__L1n__w@tch'


class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        # Y 访问首页，不小心提交了一个空待办事项
        # 输入框中没输入内容，她就按下了回车键
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys("\n")

        # 首页刷新了，显示一个错误消息
        # 提示待办事项不能为空
        # 指定使用 Bootstrap 提供的 CSS 类 .has-error 标记错误文本。Bootstrap 为这种消息提供了很多有用的样式。
        error = self.get_error_element()
        self.assertEqual(error.text, "You can't have an empty list item")

        # 她输入一些文字，然后再次提交，这次没问题了
        self.get_item_input_box().send_keys("Buy milk\n")
        self.check_for_row_in_list_table("1: Buy milk")

        # 她有点儿调皮，又提交了一个空待办事项
        self.get_item_input_box().send_keys("\n")

        # 在清单页面她看到了一个类似的错误消息
        self.check_for_row_in_list_table("1: Buy milk")
        error = self.get_error_element()
        self.assertEqual(error.text, "You can't have an empty list item")

        # 输入文字之后就没问题了
        self.get_item_input_box().send_keys("Make tea\n")
        self.check_for_row_in_list_table("1: Buy milk")
        self.check_for_row_in_list_table("2: Make tea")

    def test_cannot_add_duplicate_items(self):
        # Y 访问首页，新建一个清单
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys("Buy wellies\n")
        self.check_for_#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
这个是负责测试新到来的访问者的
"""
from base import FunctionalTest
from selenium.webdriver.common.keys import Keys
from selenium import webdriver

__author__ = '__L1n__w@tch'


class NewVisitorTest(FunctionalTest):
    def test_can_start_a_list_and_retrieve_it_later(self):
        """
        测试的主要代码写在名为 test_can_start_a_list_and_retrieve_it_later 的方法中。
        名字以 test_ 开头的方法都是测试方法, 由测试运行程序运行.
        类中可以定义多个测试方法. 为测试方法起个有意义的名字是个好主意.
        :return:
        """
        # Y 访问在线待办事项应用的首页
        # self.browser.get("http://localhost:8000") # 不用硬编码了
        self.browser.get(self.server_url)

        # Y 注意到网页的标题和头部都包含 "To-Do" 这个词
        """
        使用 self.assertIn 代替 assert 编写测试断言。
        unittest 提供了很多这种用于编写测试断言的辅助函数,如 assertEqual、assertTrue 和 assertFalse 等。
        更多断言辅助函数参见 unittest 的文档,地址是 http://docs.python.org/3/library/unittest.html。
        """
        self.assertIn("To-Do", self.browser.title)
        header_text = self.browser.find_element_by_tag_name("h1").text
        self.assertIn("To-Do", header_text)

        # 应用邀请 Y 输入一个待办事项
        input_box = self.get_item_input_box()
        self.assertEqual(
            input_box.get_attribute("placeholder"),
            "Enter a to-do item"
        )

        # Y 在一个文本框中输入了 Buy pen
        # Y 的爱好是读书
        input_box.send_keys("Buy pen")

        # Y 按下回车键后, 页面更新了
        # 待办事项表格中显示了 "1: Buy pen"
        input_box.send_keys(Keys.ENTER)
        edith_list_url = self.browser.current_url
        # assertRegex 是 unittest 中的一个辅助函数，检查字符串是否和正则表达式匹配。我们使用这个方法检查是否实现了新的 REST 式设计。
        # 具体用法参阅 [unittest 的文档](https://docs.python.org/3/library/unittest.html)
        self.assertRegex(edith_list_url, "/lists/.+")  # TestCase 里的
        self.check_for_row_in_list_table("1: Buy pen")

        # 页面中又显示了一个文本框, 可以输入其他的待办事项
        # Y 输入了 Use pen to take notes
        # Y 做事很有条理
        input_box = self.get_item_input_box()
        input_box.send_keys("Use pen to take notes")
        input_box.send_keys(Keys.ENTER)

        # 页面再次更新, 她的清单中显示了这两个待办事项
        self.check_for_row_in_list_table("1: Buy pen")
        self.check_for_row_in_list_table("2: Use pen to take notes")

        # 现在一个叫做 F 的新用户访问了网站
        ## 使用一个新浏览器会话
        ## 确保 Y 的信息不会从 cookie 中泄露出来
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # F 访问首页
        # 页面中看不到 Y 的清单
        self.browser.get(self.server_url)
        page_text = self.browser.find_element_by_tag_name("body").text
        self.assertNotIn("Buy pen", page_text)
        self.assertNotIn("Use pen to take notes", page_text)

        # F 输入一个新待办事项，新建一个清单
        input_box = self.get_item_input_box()
        input_box.send_keys("Buy milk")
        input_box.send_keys(Keys.ENTER)

        # F 获得了他唯一的 URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, "/lists/.+")
        self.assertNotEqual(francis_list_url, edith_list_url)

        # 这个页面还是没有 U 的清单
        page_text = self.browser.find_element_by_tag_name("body").text
        self.assertNotIn("Buy pen", page_text)
        self.assertIn("Buy milk", page_text)

        # Y 想知道这个网站是否会记住她的清单

        # 她看到网站为她生成了一个唯一的 URL
        # 而且页面中有一些文字解说这个功能

        # 她访问那个 URL, 发现她的待办事项列表还在
        # TODO: 这是不是还得写测试
        pass


if __name__ == "__main__":
    pass
row_in_list_table("1: Buy wellies")

        # 她不小心输入了一个重复的待办事项
        self.get_item_input_box().send_keys("Buy wellies\n")

        # 她看到一条有帮助的错误消息
        self.check_for_row_in_list_table("1: Buy wellies")
        error = self.get_error_element()
        self.assertEqual(error.text, "You've already got this in your list")

    def test_error_messages_are_cleared_on_input(self):
        # Y 新建一个清单，但方法不当，所以出现了一个验证错误
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys("\n")
        error = self.get_error_element()
        self.assertTrue(error.is_displayed())  # 1

        # 为了消除错误，她开始在输入框中输入内容
        self.get_item_input_box().send_keys("a")

        # 看到错误消息消失了，她很高兴
        error = self.get_error_element()
        self.assertFalse(error.is_displayed())  # 2

        # #1#2: is_displayed() 可检查元素是否可见。不能只靠检查元素是否存在于 DOM 中去判断，因为现在要开始隐藏元素了。
        pass

    def get_error_element(self):
        return self.browser.find_element_by_css_selector(".has-error")


if __name__ == "__main__":
    pass
