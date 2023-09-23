# -*- coding: utf-8 -*-
# version: Python3.X
"""
2023.09.23 新增第一个视图函数，实现更新
"""
import os.path

try:
    import configparser
except ImportError:
    import ConfigParser as configparser
import logging
import json
import openai
import my_constant as const
from common_module.email_send import EmailSend
from django.http import HttpResponse
from common_module.common_help_function import log_wrapper

logger = logging.getLogger("my_blog.artificial_intelligence.views")
file_path = os.path.join(os.path.dirname(__file__), "temp", "test_update.json")
cp = configparser.ConfigParser()
cp.read(const.USER_CONFIG_PATH)
openai.api_key = cp.get("email_info", "openai_key")


@log_wrapper(str_format="让 AI 更新了文件", level="info", logger=logger)
def update_file_and_send_email(request):
    try:
        if _call_chatGPT_and_update_file():
            command = f"cd {const.NOTES_PATH_PARENT_DIR} && git add {file_path} && git commit -m 'AI generate' && git push"
            os.system(command)
            es = EmailSend()
            # es.default_send_email(message="test send from Canada", logger=logger)
    except Exception as e:
        print(e)
        logger.error(e)
    finally:
        response = HttpResponse("What did you do?")
        return response


def _call_chatGPT_and_update_file():
    with open(file_path, "r") as json_file:
        data = json.load(json_file)

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": data["Question"]}
        ]
    )
    data["Answer"] = json.dumps(completion)
    with open(file_path, "w") as json_file:
        json.dump(data, json_file)
    return True
