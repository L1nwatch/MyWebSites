#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" Description
"""
from django.conf.urls import patterns, url

__author__ = '__L1n__w@tch'

urlpatterns = patterns('',
                       url(r'^login$', 'accounts.views.login', name='login'),
                       url(r'^logout$', 'accounts.views.logout', name='logout'),
                       )

if __name__ == "__main__":
    pass
