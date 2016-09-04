#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" accounts 下的 url 映射
"""
from django.conf.urls import patterns, url

__author__ = '__L1n__w@tch'

urlpatterns = patterns("",
                       url(r"^login$", "accounts.views.persona_login", name="persona_login"), )

if __name__ == "__main__":
    pass
