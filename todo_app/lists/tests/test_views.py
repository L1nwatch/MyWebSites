#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
从第 11 章开始把单元测试拆分成多个文件, 这个文件仅包含视图测试
对首页视图进行单元测试
"""

from unittest import skip
from django.test import TestCase
from django.utils.html import escape

from lists.models import Item, List
from lists.forms import ItemForm, EMPTY_LIST_ERROR, DUPLICATE_ITEM_ERROR, ExistingListItemForm

__author__ = '__L1n__w@tch'


class ListViewTest(TestCase):
    def test_displays_all_list_items(self):
        """
        测试页面是否能把所有待办事项都显示出来
        :return:
        """
        correct_list = List.objects.create()
        Item.objects.create(text="itemey 1", list_attr=correct_list)
        Item.objects.create(text="itemey 2", list_attr=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text="other item 1", list_attr=other_list)
        Item.objects.create(text="other item 2", list_attr=other_list)

        response = self.client.get("/lists/{unique_url}/".format(unique_url=correct_list.id))  # 现在不直接调用视图函数了
        # 现在不必再使用 assertIn 和 response.content.decode() 了
        # Django 提供 assertContains 方法，它知道如何处理响应以及响应内容中的字节
        self.assertContains(response, "itemey 1")
        self.assertContains(response, "itemey 2")

        self.assertNotContains(response, "other item 1")
        self.assertNotContains(response, "other item 2")

    def test_uses_list_template(self):
        """
        测试是否使用了不同的模板
        :return:
        """
        list_ = List.objects.create()
        response = self.client.get("/lists/{unique_url}/".format(unique_url=list_.id))
        self.assertTemplateUsed(response, "list.html")

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.get("/lists/{}/".format(correct_list.id))

        self.assertEqual(response.context["list_attr"], correct_list)

    def test_can_save_a_POST_request_to_an_existing_list(self):
        """
        测试发送一个 POST 请求后能够发送到正确的表单之中
        :return:
        """
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post("/lists/{unique_url}/".format(unique_url=correct_list.id),
                         data={"text": "A new item for an existing list"})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "A new item for an existing list")
        self.assertEqual(new_item.list_attr, correct_list)

    def test_POST_redirects_to_list_view(self):
        """
        测试添加完事项后会回到显示表单的 html
        :return:
        """
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            "/lists/{unique_url}/".format(unique_url=correct_list.id),
            data={"text": "A new item for an existing list"}
        )

        self.assertRedirects(response, "/lists/{unique_url}/".format(unique_url=correct_list.id))

    # def test_validation_errors_end_up_on_lists_page(self):
    #     """
    #     测试在一个清单上添加一个空项目
    #     由于测试太多, 分成以下 5 个测试了
    #     :return:
    #     """
    #     list_ = List.objects.create()
    #     response = self.client.post("/lists/{}/".format(list_.id), data={"text": ""})
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, "list.html")
    #     expected_error = escape(EMPTY_LIST_ERROR)
    #     self.assertContains(response, expected_error)

    def post_invalid_input(self):
        list_ = List.objects.create()
        return self.client.post("/lists/{}/".format(list_.id), data={"text": ""})

    def test_for_invalid_input_nothing_saved_to_db(self):
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)

    def test_for_invalid_input_renders_list_template(self):
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "list.html")

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context["form"], ExistingListItemForm)

    def test_for_invalid_input_shows_error_on_page(self):
        response = self.post_invalid_input()
        self.assertContains(response, escape(EMPTY_LIST_ERROR))

    def test_duplicate_item_validation_errors_end_up_on_lists_page(self):
        list1 = List.objects.create()

        item1 = Item.objects.create(list_attr=list1, text="textey")
        response = self.client.post("/lists/{}/".format(list1.id), data={"text": "textey"})

        expected_error = escape(DUPLICATE_ITEM_ERROR)
        self.assertContains(response, expected_error)
        self.assertTemplateUsed(response, "list.html")
        self.assertEqual(Item.objects.all().count(), 1)

    def test_displays_item_form(self):
        list_ = List.objects.create()
        response = self.client.get("/lists/{}/".format(list_.id))
        self.assertIsInstance(response.context["form"], ExistingListItemForm)
        self.assertContains(response, 'name="text"')


class NewListTest(TestCase):
    def test_saving_a_POST_request(self):
        """
        测试页面是否能够保存 POST 请求, 并且能够把用户提交的待办事项保存到表格中
        :return:
        """
        self.client.post("/lists/new", data={"text": "A new list item"})

        # 检查是否把一个新 Item 对象存入数据库。objects.count() 是 objects.all().count() 的简写形式。
        self.assertEqual(Item.objects.count(), 1, "希望数据库中现在有 1 条数据, 然而却有 {} 条数据".format(Item.objects.count()))
        new_item = Item.objects.first()  # objects.first() 等价于 objects.all()[0]
        self.assertEqual(new_item.text, "A new list item")  # 检查待办事项的文本是否正确

    def test_redirects_after_POST(self):
        """
        测试在发送 POST 请求后是否会重定向
        :return:
        """
        response = self.client.post("/lists/new", data={"text": "A new list item"})
        new_list = List.objects.first()

        self.assertEqual(response.status_code, 302, "希望返回 302 代码, 然而却返回了 {}".format(response.status_code))
        self.assertEqual(response["location"], "/lists/{unique_url}/".format(unique_url=new_list.id))
        self.assertRedirects(response, "/lists/{unique_url}/".format(unique_url=new_list.id))  # 等价于上面两条

    # def test_validation_errors_are_sent_back_to_home_page_template(self):
    #     """
    #     测试添加一个空事项时会有提示
    #     这里测试的项目太多了, 拆分成下面 2 个了.
    #     :return:
    #     """
    #     response = self.client.post("/lists/new", data={"text": ""})
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, "home.html")
    #     excepted_error = EMPTY_LIST_ERROR
    #     # excepted_error = "You can&#39;t have an empty list item" # 硬编码打出单引号
    #     # self.assertContains(response, excepted_error)
    #     self.assertContains(response, escape(excepted_error))

    def test_for_invalid_input_renders_home_template(self):
        """
        如果有验证错误，应该渲染首页模板，并且返回 200 响应
        :return:
        """
        response = self.client.post("/lists/new", data={"text": ""})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")

    def test_validation_errors_are_shown_on_home_page(self):
        """
        如果有验证错误，响应中应该包含错误信息
        :return:
        """
        response = self.client.post("/lists/new", data={"text": ""})
        self.assertContains(response, escape(EMPTY_LIST_ERROR))

    def test_for_invalid_input_passes_form_to_template(self):
        """
        如果有验证错误，应该把表单对象传入模板
        :return:
        """
        response = self.client.post("/lists/new", data={"text": ""})
        self.assertIsInstance(response.context["form"], ItemForm)

    def test_invalid_list_items_are_not_saved(self):
        """
        确保不会保存空待办事项
        :return:
        """
        self.client.post("/lists/new", data={"text": ""})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(List.objects.count(), 0)


class HomePageTest(TestCase):
    maxDiff = None  # 默认情况下会解决较长的差异，需要进行设置

    # def test_root_url_resolves_to_home_page_view(self):
    #     """
    #     测试访问根路径时是由 home_page 视图函数来负责相关处理的
    #     :return:
    #     """
    #     found = resolve("/")  # resolve 是 Django 内部使用的函数，用于解析 URL，并将其映射到对应的视图函数上。
    #     self.assertEqual(found.func, home_page)  # 检查解析网站根路径"/"时，是否能找到名为 home_page 的函数

    # def test_home_page_returns_correct_html(self):
    #     """
    #     测试访问主页时得到的是一个正确的 html 文本
    #     :return:
    #     """
    #     request = HttpRequest()  # 创建了一个 HttpRequest 对象，用户在浏览器中请求网页时，Django 看到的就是 HttpRequest 对象。
    #
    #     response = home_page(request)  # 把这个 HttpRequest 对象传给 home_page 视图，得到响应。
    #
    #     excepted_html = render_to_string("home.html", {"form": ItemForm()}, request=request)
    #     # self.assertEqual(response.content.decode("utf8"), excepted_html)
    #
    #     # 对比长字符串时 assertMultiLineEqual 很有用，它会以差异的格式显示输出
    #     self.assertMultiLineEqual(response.content.decode(), excepted_html)

    def test_home_page_renders_home_template(self):
        response = self.client.get("/")
        # 使用辅助方法 assertTemplateUsed 替换之前手动测试模板的 diamante
        self.assertTemplateUsed(response, "home.html")

    def test_home_page_uses_item_form(self):
        response = self.client.get("/")
        # 使用 assertIsInstance 确认视图使用的是正确的表单类
        self.assertIsInstance(response.context["form"], ItemForm)


class MyListsTest(TestCase):
    def test_my_lists_url_renders_my_lists_template(self):
        response = self.client.get("/lists/users/a@b.com/")
        self.assertTemplateUsed(response, "my_lists.html")
