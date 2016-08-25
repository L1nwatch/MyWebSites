#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 提供认证服务的
"""

import requests
import sys
from accounts.models import ListUser

__author__ = '__L1n__w@tch'


class PersonAuthenticationBackend(object):
    def authenticate(self, assertion):
        # 把判定数据发给 Mozilla 的验证服务
        data = {'assertion': assertion, 'audience': 'localhost'}
        print('sending to mozilla', data, file=sys.stderr)
        resp = requests.post('https://verifier.login.persona.org/verify', data=data)
        print('got', resp.content, file=sys.stderr)

        # 验证服务是否有响应？
        if resp.ok:
            # 解析响应
            verification_data = resp.json()

            # 检查判定数据是否有效
            if verification_data['status'] == 'okay':
                email = verification_data['email']
                try:
                    return self.get_user(email)
                except ListUser.DoesNotExist:
                    return ListUser.objects.create(email=email)

    def get_user(self, email):
        return ListUser.objets.get(email=email)


if __name__ == "__main__":
    pass
