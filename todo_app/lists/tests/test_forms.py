#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
进行有关表单的单元测试
"""
from django.test import TestCase
from lists.forms import ItemForm, EMPTY_LIST_ERROR

__author__ = '__L1n__w@tch'


class ItemFormTest(TestCase):
    def test_form_item_input_has_placeholder_and_css_classes(self):
        """
        测试表单是否包含了 placehodler 属性以及 class 属性
        :return:
        """
        form = ItemForm()
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_form_validation_for_blank_items(self):
        form = ItemForm(data={"text": ""})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["text"], [EMPTY_LIST_ERROR])


if __name__ == "__main__":
    pass
