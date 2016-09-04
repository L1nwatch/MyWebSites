#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" Description
"""
from django.test import TestCase
from django.contrib.auth import get_user_model

__author__ = '__L1n__w@tch'

User = get_user_model()


class UserModelTest(TestCase):
    def test_user_is_valid_with_email_only(self):
        user = User(email="a@b.com")
        user.full_clean()  # 不该抛出异常


if __name__ == "__main__":
    pass
