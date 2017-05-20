#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 负责对日志进行打包

2017.05.20 开始编写基本功能, 即打包日志
"""
import os
import zipfile
import datetime

__author__ = '__L1n__w@tch'


class LogPacker:
    def __init__(self, log_path):
        """
        :param log_path: str(), log 文件的根目录, 比如 "/home/watch/sites/watch0.top/log"
        """
        self.log_path = log_path

    def run(self):
        """
        实现打包功能, 打包指定目录下所有以 log 结尾的文件, 打包完成后将现有内容清空:
            1. 遍历每一个 log 文件, 读取文件内容, 并清空文件
            2. 为每个 log 文件新建一个格式为 日期_log文件名.log 的备份文件, 并将读取到的内容存入进去
            3. 将所有同一日期的备份文件打包到同一个压缩包中, 压缩包以 日期_log 命名
        """
        now = datetime.datetime.today()
        yesterday = now - datetime.timedelta(days=1)
        zip_file_name = "{}{}{}_log.zip".format(yesterday.year, yesterday.month, yesterday.day)
        zip_file_path = os.path.join(self.log_path, zip_file_name)

        # 还没为昨天打包过, 则执行打包操作
        if not os.path.exists(zip_file_path):
            with zipfile.ZipFile(zip_file_path, "w") as my_zip:
                for each_file in (x for x in os.listdir(self.log_path) if x.endswith(".log")):
                    file_path = os.path.join(self.log_path, each_file)
                    my_zip.write(file_path, each_file, compress_type=zipfile.ZIP_DEFLATED)
                    with open(file_path, "w") as f:
                        pass


if __name__ == "__main__":
    pass
