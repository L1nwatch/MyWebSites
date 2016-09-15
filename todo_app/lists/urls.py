#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" Description
"""
from django.conf.urls import url
import lists.views

__author__ = '__L1n__w@tch'

urlpatterns = [
    url(r"^(\d+)/$", lists.views.view_list, name="view_list"),
    url(r"^new$", lists.views.new_list2, name="new_list"),
    url(r"^users/(.+)/$", lists.views.my_lists, name="my_lists")
]

if __name__ == "__main__":
    pass
