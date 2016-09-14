#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
表单
"""
from django import forms
from django.core.exceptions import ValidationError

from lists.models import Item, List

__author__ = '__L1n__w@tch'

EMPTY_LIST_ERROR = "You can't have an empty list item"
DUPLICATE_ITEM_ERROR = "You've already got this in your list"


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


class ExistingListItemForm(ItemForm):
    def __init__(self, for_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.list_attr = for_list

    def validate_unique(self):
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            e.error_dict = {'text': [DUPLICATE_ITEM_ERROR]}
            self._update_errors(e)

    def save(self):
        return forms.models.ModelForm.save(self)


class NewListForm(ItemForm):
    pass


if __name__ == "__main__":
    pass
