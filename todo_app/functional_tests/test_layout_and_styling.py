#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
针对布局和样式的功能测试
"""
from .base import FunctionalTest

__author__ = '__L1n__w@tch'


class LayoutAndStylingTest(FunctionalTest):
    def test_layout_and_styling(self):
        # Y 访问首页
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024, 768)

        # 她看到输入框完美地居中显示
        input_box = self.get_item_input_box()
        self.assertAlmostEqual(input_box.location["x"] + input_box.size["width"] / 2, 512, delta=5)

        # 她新建了一个清单，看到输入框仍完美地居中显示
        input_box.send_keys("I make a new item\n")  # 两种写法, 一种手动加 \n, 一种发送 ENTER 键
        # input_box.send_keys(Keys.ENTER)

        input_box = self.get_item_input_box()
        self.assertAlmostEqual(input_box.location["x"] + input_box.size["width"] / 2, 512, delta=5)

        self.fail("test")


if __name__ == "__main__":
    pass
