#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" Description
"""

__author__ = '__L1n__w@tch'


class HomePage(object):
    def __init__(self, test):
        # 使用表示当前测试的对象初始化，这样就能声明断言，通过 self.test.browser 访问浏览器实例，也能使用 wait_for 函数
        self.test = test

    # 大多数页面对象都有一个方法用于访问这个页面。注意，这个方法实现了交互等待模式——首先调用 get 方法获取这个页面的 URL，然后等待我们知道会在首页中显示的元素出现
    def go_to_home_page(self):
        self.test.browser.get(self.test.server_url)
        self.test.wait_for(self.get_item_input)
        return self  # 返回 self 只是为了操作方便。这么做可以使用方法串接 https://en.wikipedia.org/wiki/ Method_chaining

    def get_item_input(self):
        return self.test.browser.find_element_by_id("id_text")

    # 这是用于新建清单的方法。访问首页，找到输入框，再按回车键。然后等待一段时间，确保交互完成。不过可以看出，这次等待其实发生在另一个页面对象中
    def start_new_list(self, item_text):
        self.go_to_home_page()
        inputbox = self.get_item_input()
        inputbox.send_keys(item_text + "\n")
        # ListPage 稍后定义，初始化的方式类似于 HomePage
        list_page = ListPage(self.test)
        # 调用 ListPage 类中的 wait_for_new_item_in_list 方法，指定期望看到的待办事项文本以及在清单中的排位
        list_page.wait_for_new_item_in_list(item_text, 1)
        return list_page  # 最后，把 list_page 对象返回给调用者，因为调用者可能会用到这个对象

    def go_to_my_lists_page(self):
        self.test.browser.find_element_by_link_text("My Lists").click()
        self.test.wait_for(lambda: self.test.assertEqual(
            self.test.browser.find_element_by_tag_name("h1").text,
            "My Lists"
        ))


class ListPage(object):
    def __init__(self, test):
        self.test = test

    def get_list_table_rows(self):
        return self.test.browser.find_elements_by_css_selector("#id_list_table tr")

    def wait_for_new_item_in_list(self, item_text, position):
        expected_row = "{}: {}".format(position, item_text)
        self.test.wait_for(lambda: self.test.assertIn(
            expected_row,
            [row.text for row in self.get_list_table_rows()]
        ))

    def get_share_box(self):
        return self.test.browser.find_element_by_css_selector("input[name=email]")

    def get_shared_with_list(self):
        return self.test.browser.find_element_by_css_selector(".list-sharee")

    def share_list_with(self, email):
        self.get_share_box().send_keys(email + "\n")
        self.test.wait_for(lambda: self.test.assertIn(email, [item.text for item in self.get_shared_with_list()]))


if __name__ == "__main__":
    pass
