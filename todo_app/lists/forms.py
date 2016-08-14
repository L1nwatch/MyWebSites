#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
表单
"""
from django import forms
from lists.models import Item

__author__ = '__L1n__w@tch'

EMPTY_LIST_ERROR = "You can't have an empty list item"


class ItemForm(forms.models.ModelForm):
    class Meta:
        model = Item
        fields = ("text",)  # 注意逗号不可省略, 因为要表示成元组
        widgets = {
            "text": forms.fields.TextInput(attrs={
                "placeholder": "Enter a to-do item",
                "class": "form-control input-lg"
            })
        }
        error_messages = {
            "text": {"required": EMPTY_LIST_ERROR}
        }

    def save(self, for_list):
        self.instance.list_attr = for_list
        return super().save()


if __name__ == "__main__":
    pass
