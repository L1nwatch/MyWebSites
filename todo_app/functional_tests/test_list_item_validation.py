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
        self.check_for_row_in_list_table("1: Buy wellies")

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
