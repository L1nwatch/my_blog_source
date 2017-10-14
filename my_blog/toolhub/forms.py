#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 编写相关的 form

2017.10.14 复制了一个 form 给凯撒密码用的
2017.03.25 新增 textarea 表单, 用于 GitHub 图片地址转换用的
"""
from django import forms

__author__ = '__L1n__w@tch'


class CaesarCipherTextareaForm(forms.Form):
    input_area = forms.CharField(label="", widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["input_area"].widget.attrs.update({
            "autofocus": True,
            "id": "id_input_box",
            "placeholder": "请输入你要解密的数据",
            "spellcheck": False
        })

class GitHubTranslateTextareaForm(forms.Form):
    input_area = forms.CharField(label="", widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["input_area"].widget.attrs.update({
            "autofocus": True,
            "id": "id_input_box",
            "placeholder": "请输入你要转换的数据",
            "spellcheck": False
        })


if __name__ == "__main__":
    pass
