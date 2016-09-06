#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 自定义认证函数
"""

import requests
# import logging
from django.contrib.auth import get_user_model

__author__ = '__L1n__w@tch'

PERSONA_VERIFY_URL = "https://verifier.login.persona.org/verify"
DOMAIN = "localhost"
User = get_user_model()


class PersonaAuthenticationBackend(object):
    def authenticate(self, assertion):
        logging.warning("entering authenticate function")
        response = requests.post(
            PERSONA_VERIFY_URL,
            data={"assertion": assertion, "audience": DOMAIN}
        )

        logging.warning("got response from persona")
        logging.warning(response.content.decode())

        if response.ok and response.json()["status"] == "okay":
            email = response.json()["email"]
            try:
                return User.objects.get(email=email)
            except User.DoesNotExist:
                return User.objects.create(email=email)

    def get_user(self, email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None


if __name__ == "__main__":
    pass
