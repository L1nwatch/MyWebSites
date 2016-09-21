#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
从第 11 章开始把单元测试拆分成多个文件, 这个文件仅包含视图测试
对首页视图进行单元测试
"""

import unittest
from unittest.mock import Mock, patch

from django.test import TestCase
from django.utils.html import escape
from django.http import HttpRequest
from django.contrib.auth import get_user_model

from lists.models import Item, List
from lists.views import new_list
from lists.forms import ItemForm, EMPTY_LIST_ERROR, DUPLICATE_ITEM_ERROR, ExistingListItemForm, NewListForm

__author__ = '__L1n__w@tch'

User = get_user_model()


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


# 本来说是要把整个 NewListTest 重命名的, 不过我想想还是算了吧
class NewListViewIntegratedTest(TestCase):
    def test_list_owner_is_saved_if_user_is_authenticated(self):
        request = HttpRequest()
        request.user = User.objects.create(email="a@b.com")
        request.POST["text"] = "new list item"
        new_list(request)
        list_ = List.objects.first()
        self.assertEqual(list_.owner, request.user)

    @unittest.skip  # 尝试使用驭件保存属主的测试, 太过复杂, 用上面这个替代
    @patch("lists.views.List")  # 模拟 List 模型的功能，获取视图创建的任何一个清单
    def test_mock_list_owner_is_saved_if_user_is_authenticated(self, mockList):
        # 为视图创建一个真实的 List 对象。List 对象必须真实，否则视图尝试保存 Item 对象时会遇到外键错误(表明这个测试只是部分隔离)
        mock_list = List.objects.create()
        mock_list.save = Mock()
        mockList.return_value = mock_list
        request = HttpRequest()
        request.user = User.objects.create()  # 给 requests 对象赋值一个真实的用户
        request.POST["text"] = "new list item"
        new_list(request)
        self.assertEqual(mock_list.owner, request.user)  # 现在可以声明断言，判断清单对象是否设定了 .owner 属性

        mock_list = List.objects.create()
        mock_list.save = Mock()
        mockList.return_value = mock_list
        request = HttpRequest()
        request.user = Mock()
        request.user.is_authenticated.return_value = True
        request.POST["text"] = "new list item"

        # 定义一个函数，在这个函数中就希望先发生的事件声明断言，即检查是否设定了清单的属主
        def check_owner_assigned():
            self.assertEqual(mock_list.owner, request.user)

        # 把这个检查函数赋值给后续事件的 side_effect 属性。当视图在驭件上调用 save 方法时，才会执行其中的断言。要保证在测试的目标函数调用前完成此次赋值
        mock_list.save.side_effect = check_owner_assigned
        new_list(request)
        # 最后，要确保设定了 side_effect 属性的函数一定会被调用，也就是要调用 .save() 方法。否则断言永远不会运行
        mock_list.save.assert_called_once_with()

        # def test_list_owner_is_saved_if_user_is_authenticated(self):
        #     request = HttpRequest()
        #     request.user = User.objects.create(email="a@b.com")
        #     request.POST["text"] = "new list item"
        #     new_list(request)
        #     list_ = List.objects.first()
        #     self.assertEqual(list_.owner, request.user)


@patch("lists.views.NewListForm")  # 模拟 NewListForm 类。类中的所有测试方法都会用到这个驭件，所以在类上模拟
# 使用 Django 提供的 TestCase 类太容易写成整合测试。为了确保写出纯粹隔离的单元测试，只能使用 unittest.TestCase
class NewListViewUnitTest(unittest.TestCase):
    def setUp(self):
        self.request = HttpRequest()
        # 在 setUp 方法中手动创建了一个简单的 POST 请求，没有使用(太过整合的) Django 测试客户端
        self.request.POST["text"] = "new list item"
        self.request.user = Mock()

    def test_passes_POST_data_to_NewListForm(self, mockNewListForm):
        new_list(self.request)
        # 然后检查视图要做的第一件事：在视图中使用正确的构造方法初始化它的协作者，即 NewListForm，传入的数据从请求中读取
        mockNewListForm.assert_called_once_with(data=self.request.POST)

    def test_saves_form_with_owner_if_form_valid(self, mockNewListForm):
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = True
        new_list(self.request)
        mock_form.save.assert_called_once_with(owner=self.request.user)

    @patch("lists.views.redirect")  # 模拟 redirect 函数，这次直接在方法上模拟
    # patch 修饰器先应用最内层的那个，所以这个驭件在 mockNewListForm 之前传入方法
    def test_redirects_to_form_returned_object_if_form_valid(self, mock_redirect, mockNewListForm):
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = True  # 指定测试的是表单中数据有效的情况

        response = new_list(self.request)

        self.assertEqual(response, mock_redirect.return_value)  # 检查视图的响应是否为 redirect 函数的结果
        # 然后检查调用 redirect 函数时传入的参数是否为在表单上调用 save 方法得到的对象
        # 模拟的 form.save 方法返回一个对象，我们希望在视图中使用这个对象。
        mock_redirect.assert_called_once_with(mock_form.save.return_value)

    @patch("lists.views.render")
    def test_renders_home_template_with_form_if_form_invalid(self, mock_render, mockNewListForm):
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = False
        response = new_list(self.request)
        self.assertEqual(response, mock_render.return_value)
        mock_render.assert_called_once_with(self.request, "home.html", {"form": mock_form})

    def test_does_not_save_if_form_invalid(self, mockNewListForm):
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = False
        new_list(self.request)
        self.assertFalse(mock_form.save.called)


@unittest.skip
class NewListFormTest(unittest.TestCase):
    # 为表单模拟两个来自下部模型层的协作者
    @patch("lists.forms.List")
    @patch("lists.forms.Item")
    def test_save_creates_new_list_and_item_from_post_data(self, mockItem, mockList):
        mock_item = mockItem.return_value
        mock_list = mockList.return_value
        user = Mock()
        form = NewListForm(data={"text": "new item text"})
        form.is_valid()  # 必须调用 is_valid 方法，这样表单才会把通过验证的数据存储到 .cleaned_data 字典中

        def check_item_text_and_list():
            self.assertEqual(mock_item.text, "new item text")
            self.assertEqual(mock_item.list, mock_list)
            self.assertTrue(mock_list.save.called)
            mock_item.save.side_effect = check_item_text_and_list  # 使用 side_effect 方法确保保存新待办事项对象时，使用已经保存的清单，而且待办事项中的文本正确
            form.save(owner=user)

        self.assertTrue(mock_item.save.called)  # 再次确认调用了副作用函数


class ShareListTest(TestCase):
    def test_post_redirects_to_lists_page(self):
        list1 = List.objects.create()
        response = self.client.post("/lists/{}/share".format(list1.id), data={"email": "test2@email.com"})
        self.assertRedirects(response, list1.get_absolute_url())

    def test_post_share_email_correct(self):
        user = User.objects.create(email="test@email.com")
        list1 = List.objects.create()
        response = self.client.post("/lists/{}/share".format(list1.id), data={"email": user.email})
        self.assertIn(user, list1.shared_with.all())


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
        User.objects.create(email="a@b.com")
        response = self.client.get("/lists/users/a@b.com/")
        self.assertTemplateUsed(response, "my_lists.html")

    def test_passes_correct_owner_to_template(self):
        User.objects.create(email="wrong@owner.com")
        correct_user = User.objects.create(email="a@b.com")
        response = self.client.get("/lists/users/a@b.com/")
        self.assertEqual(response.context["owner"], correct_user)
