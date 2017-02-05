#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
"""
2017.02.05 作为吃货的一个 APP 放上来了
"""
from django.conf.urls import url
import just_eating.views

__author__ = '__L1n__w@tch'

urlpatterns = [
    url(r"^$", just_eating.views.just_eating_home_view, name="just_eating"),
]

if __name__ == "__main__":
    pass
