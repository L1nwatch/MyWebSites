#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
这个文件只包含模型测试
"""
from django.test import TestCase
from lists.models import Item, List
from django.core.exceptions import ValidationError


__author__ = '__L1n__w@tch'


class ListAndItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = "The first (ever) list item"
        first_item.list_attr = list_
        first_item.save()

        second_item = Item()
        second_item.text = "Item the second"
        second_item.list_attr = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, "The first (ever) list item")
        self.assertEqual(first_saved_item.list_attr, list_)
        self.assertEqual(second_saved_item.text, "Item the second")
        self.assertEqual(second_saved_item.list_attr, list_)

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


if __name__ == "__main__":
    pass
