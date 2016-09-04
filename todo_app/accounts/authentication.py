#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 自定义认证函数
"""

import requests
from django.contrib.auth import get_user_model

__author__ = '__L1n__w@tch'

PERSONA_VERIFY_URL = "https://verifier.login.persona.org/verify"
DOMAIN = "localhost"
User = get_user_model()


class PersonaAuthenticationBackend(object):
    def authenticate(self, assertion):
        response = requests.post(
            PERSONA_VERIFY_URL,
            data={"assertion": assertion, "audience": DOMAIN}
        )

        if response.ok and response.json()["status"] == "okay":
            return User.objects.get(email=response.json()["email"])


if __name__ == "__main__":
    pass
