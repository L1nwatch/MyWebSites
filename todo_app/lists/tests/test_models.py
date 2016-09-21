#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
这个文件只包含模型测试
"""
from lists.models import Item, List

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.contrib.auth import get_user_model

__author__ = '__L1n__w@tch'

User = get_user_model()


class ListModelTest(TestCase):
    def test_get_absolute_url(self):
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), "/lists/{}/".format(list_.id))

    def test_create_new_creates_list_and_first_item(self):
        List.create_new(first_item_text="new item text")
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "new item text")
        new_list = List.objects.first()
        self.assertEqual(new_item.list_attr, new_list)

    def test_create_new_optionally_saves_owner(self):
        user = User.objects.create()
        List.create_new(first_item_text="new item text", owner=user)
        new_list = List.objects.first()
        self.assertEqual(new_list.owner, user)

    def test_lists_can_have_owners(self):
        List(owner=User())  # 不该抛出异常

    def test_list_owner_is_optional(self):
        List().full_clean()  # 不该抛出异常

    def test_create_returns_new_list_object(self):
        returned = List.create_new(first_item_text="new item text")
        new_list = List.objects.first()
        self.assertEqual(returned, new_list)

    def test_list_name_is_first_item_text(self):
        list_ = List.objects.create()
        Item.objects.create(list_attr=list_, text="first item")
        Item.objects.create(list_attr=list_, text="second item")
        self.assertEqual(list_.name, "first item")

    def test_shared_wtih_add_and_all(self):
        # 检查清单能否响应 shared_with.add 方法
        list1 = List.objects.create()
        test_email = "test@email.com"
        user = User.objects.create(email=test_email)
        list1.shared_with.add(test_email)
        list_in_db = List.objects.get(id=list1.id)
        self.assertIn(user, list_in_db.shared_with.all())


class ItemModelTest(TestCase):
    def test_default_text(self):
        item = Item()
        self.assertEqual(item.text, "")

    def test_item_is_related_to_list(self):
        list_ = List.objects.create()
        item = Item()
        item.list_attr = list_
        item.save()
        self.assertIn(item, list_.item_set.all())

    def test_cannot_save_empty_list_items(self):
        list_ = List.objects.create()
        item = Item(list_attr=list_, text="")
        # 这是一个新的单元测试技术，如果想检查做某件事是否会抛出异常，可以使用 self.assertRaises 上下文管理器。
        # 此处还可写成：
        # try:
        #     item.save()
        #     item.full_clean()
        #     self.fail("The save should have raised an exception")
        # except ValidationError:
        #     pass
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_duplicate_items_are_invalid(self):
        list_ = List.objects.create()
        Item.objects.create(list_attr=list_, text="bla")
        with self.assertRaises(ValidationError):
            item = Item(list_attr=list_, text="bla")
            item.full_clean()
            # item.save() # SQLite 会报错

    def test_CAN_save_same_item_to_different_lists(self):
        list1 = List.objects.create()
        list2 = List.objects.create()
        Item.objects.create(list_attr=list1, text="bla")
        item = Item(list_attr=list2, text="bla")
        item.full_clean()  # 不该抛出异常

    def test_list_ordering(self):
        list1 = List.objects.create()
        item1 = Item.objects.create(list_attr=list1, text="i1")
        item2 = Item.objects.create(list_attr=list1, text="item 2")
        item3 = Item.objects.create(list_attr=list1, text="3")

        # 也可以考虑使用 unittest 中的 assertSequenceEqual, 以及 Django 测试工具箱中的 assertQuerysetEqual
        self.assertEqual(
            list(Item.objects.all()),
            [item1, item2, item3]
        )

    def test_string_representation(self):
        item = Item(text="some text")
        self.assertEqual(str(item), "some text")


if __name__ == "__main__":
    pass
