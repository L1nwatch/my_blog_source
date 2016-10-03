#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
使用 Django 的管理命令来绕过认证
"""
from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
from django.contrib.sessions.backends.db import SessionStore
from django.core.management.base import BaseCommand

__author__ = '__L1n__w@tch'

User = get_user_model()


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('email')

    def handle(self, *args, **kwargs):
        email = kwargs["email"]
        session_key = create_pre_authenticated_session(email)
        self.stdout.write(session_key)


def create_pre_authenticated_session(email):
    user = User.objects.create(email=email)
    session = SessionStore()
    session[SESSION_KEY] = user.pk
    session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
    session.save()
    return session.session_key


if __name__ == "__main__":
    pass
