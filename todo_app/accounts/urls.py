#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" accounts 下的 url 映射
"""
from django.conf.urls import url
import django.contrib.auth.views
import accounts.views

__author__ = '__L1n__w@tch'

urlpatterns = [
    url(r"^login$", accounts.views.persona_login, name="persona_login"),
    url(r"^logout$", django.contrib.auth.views.logout, {"next_page": "/"}, name="logout"),
]

if __name__ == "__main__":
    pass
