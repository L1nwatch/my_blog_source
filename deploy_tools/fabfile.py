#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 使用 Fabric 进行自动化部署
"""
import random
import string
import os
from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run, sudo

__author__ = '__L1n__w@tch'

# 要把常量 REPO_URL 的值改成代码分享网站中你仓库的 URL
REPO_URL = "https://github.com/L1nwatch/my_blog_source.git"


def deploy():
    """
    2016.10.04 根据之前的自动化部署代码进行更改, 这里要进行的几个操作包括:
        创建文件夹目录,获取最新版本代码,更新 settings 文件, 更新 Python 虚拟环境, 更新静态文件, 更新数据库, 设置 nginx 和 gunicorn
    :return:
    """
    # env.host 的值是在命令行中指定的服务器地址，例如 watch0.top, env.user 的值是登录服务器时使用的用户名
    site_folder = "/home/{}/sites/{}".format(env.user, env.host)
    source_folder = os.path.join(site_folder, "source")
    virtualenv_folder = os.path.join(source_folder, "../virtualenv")
    site_name = "my_blog"
    host_name = env.host
    user = env.user

    # 创建结构树
    _create_directory_structure_if_necessary(site_folder)

    # 更新代码
    _get_latest_source(source_folder)

    # 更新 setting 文件
    _update_settings(source_folder, site_name, host_name)

    # 更新虚拟环境以及所需的各个包
    _update_virtualenv(source_folder, virtualenv_folder)

    # 打包 static 文件
    _update_static_files(source_folder, virtualenv_folder, site_name)

    # 数据库迁移
    _update_database(source_folder, virtualenv_folder, site_name)

    # 设置服务器配置等
    _set_nginx_gunicorn(source_folder, host_name, site_name, user)


def _create_directory_structure_if_necessary(site_folder):
    for sub_folder in ["virtualenv"]:
        # run 的作用是在服务器中执行指定的 shell 命令
        # mkdir -p 是 mkdir 的一个有用变种，它有两个优势，其一是深入多个文件夹层级创建目录；其二，只在必要时创建目录。
        run("mkdir -p {}/{}".format(site_folder, sub_folder))


def _get_latest_source(source_folder):
    # exists 检查服务器中是否有指定的文件夹或文件。我们指定的是隐藏文件夹 .git，检查仓库是否已经克隆到文件夹中。
    if exists(source_folder + "/.git"):
        # 很多命令都以 cd 开头，其目的是设定当前工作目录。Fabric 没有状态记忆，所以下次运行 run 命令时不知道在哪个目录中
        # 在现有仓库中执行 git fetch 命令是从网络中拉取最新提交
        run("cd {} && git fetch".format(source_folder))
    else:
        # 如果仓库不存在，就执行 git clone 命令克隆一份全新的源码。
        run("git clone {} {}".format(REPO_URL, source_folder))
    # Fabric 中的 local 函数在本地电脑中执行命令，这个函数其实是对 subprocess.Popen 的再包装。
    # 我们捕获 git log 命令的输出，获取本地仓库中当前提交的哈希值，这么做的结果是，服务器中代码将和本地检出的代码版本一致

    current_commit = local("git log -n 1 --format=%H", capture=True)
    # 执行 git reset --hard 命令，切换到指定的提交。这个命令会撤销在服务器中对代码仓库所做的任何改动。
    run("cd {} && git reset --hard {}".format(source_folder, current_commit))

    # 发现书中给的没法获取最新版本, 所以自己又多添加了一条来进行确保
    run("cd {} && git pull".format(source_folder, current_commit))


def _update_settings(source_folder, site_name, host_name):
    settings_path = source_folder + "/{site_name}/{site_name}/settings.py".format(site_name=site_name)
    # Fabric 提供的 sed 函数作用是在文本中替换字符串。这里把 DEBUG 的值由 True 改成 False
    sed(settings_path, "DEBUG = True", "DEBUG = False")
    # 这里使用 sed 调整 ALLOWED_HOSTS 的值，使用正则表达式匹配正确的代码行
    sed(settings_path, 'DOMAIN = "localhost"', 'DOMAIN = "{}"'.format(host_name))
    secret_key_file = source_folder + "/{site_name}/{site_name}/secret_key.py".format(site_name=site_name)

    # Django 有几处加密操作要使用 SECRET_KEY: cookie 和 CSRF 保护。在服务器中和(可能公开的)源码仓库中使用不同的密钥是个好习惯。
    # 如果还没有密钥，这段代码会生成一个新密钥，然后写入密钥文件。有密钥后，每次部署都要使用相同的密钥。
    # 更多信息参见 [Django 文档](https://docs.djangoproject.com/en/1.7/topics/signing/)
    if not exists(secret_key_file):
        chars = string.ascii_letters + string.digits + "!@#$%^&*(-_=+)"
        key = "".join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, "SECRET_KEY = '{}'".format(key))
    # append 的作用是在文件末尾添加一行内容
    # (如果要添加的行已经存在，就不会再次添加；但如果文件末尾不是一个空行，它却不能自动添加一个空行。因此加上了 \n。)
    # 使用的是 "相对导入"(relative import，使用 from .secret key 而不是 from secret_key)
    # 目的是确保从本地而不是从 sys.path 中其他位置的模块导入。
    append(settings_path, "\nfrom .secret_key import SECRET_KEY")


def _update_virtualenv(source_folder, virtualenv_folder):
    # 在 virtualenv 文件夹中查找可执行文件 pip，以检查虚拟环境是否存在
    if not exists(virtualenv_folder + "/bin/pip"):
        run("virtualenv --python=python3 {}".format(virtualenv_folder))
    # 然后和之前一样，执行 pip install -r 命令
    run("{virtualenv_folder}/bin/pip install -r {source_folder}/virtual/requirements.txt"
        .format(virtualenv_folder=virtualenv_folder, source_folder=source_folder))


def _update_static_files(source_folder, virtualenv_folder, site_name):
    # 如果需要执行 Django 的 manage.py 命令，就要指定虚拟环境中二进制文件夹，确保使用的是虚拟环境中的 Django 版本，而不是系统中的版本
    run("cd {source_folder} && {virtualenv_folder}/bin/python3 {site_name}/manage.py collectstatic --noinput"
        .format(source_folder=source_folder, virtualenv_folder=virtualenv_folder, site_name=site_name))


def _update_database(source_folder, virtualenv_folder, site_name):
    run("cd {source_folder} && {virtualenv_folder}/bin/python3 {site_name}/manage.py makemigrations --noinput"
        .format(source_folder=source_folder, virtualenv_folder=virtualenv_folder, site_name=site_name))
    run("cd {source_folder} && {virtualenv_folder}/bin/python3 {site_name}/manage.py migrate --noinput"
        .format(source_folder=source_folder, virtualenv_folder=virtualenv_folder, site_name=site_name))


def _set_nginx_gunicorn(source_folder, host_name, site_name, user):
    """
    利用 sed 来配置 nginx 以及 gunicorn
    # 这里，使用 "s/replace_me/with_this/g" 句法把字符串 SITE_NAME 替换成网站名, 还有主机名和用户名也类似。
    # 然后使用管道操作（|）把文本流传给一个有 root 权限的用户处理（sudo），把传入的文本流写入一个文件
    # 即 sites-available 文件夹中的一个虚拟主机配置文件。
    # 这里可以用 sudo() 替代 run() 这样就可以在命令行中指定 sudo 密码不用每次都手打了
    :param source_folder: 文件夹路径
    :param host_name: 主机名, 比如 "watch0.top"
    :param site_name: 网站名, 比如 "my_blog"
    :param user: 用户名, 比如 "watch"
    :return:
    """
    # 编写 nginx 配置文件
    sudo('cd {}'
         ' && sed "s/HOST_NAME/{host}/g" deploy_tools/nginx.template.conf'
         ' | sed "s/USER_NAME/{user}/g"'
         ' | tee /etc/nginx/sites-available/{host}'
         .format(source_folder, host=host_name, user=user))

    # 激活这个文件配置的虚拟主机
    sudo('ln -sf /etc/nginx/sites-available/{host} /etc/nginx/sites-enabled/{host}'.format(host=host_name))

    # 编写 Upstart 脚本
    sudo('cd {}'
         ' && sed "s/HOST_NAME/{host}/g" deploy_tools/gunicorn-upstart.template.conf'
         ' | sed "s/USER_NAME/{user}/g"'
         ' | sed "s/SITE_NAME/{site_name}/g"'
         ' | tee /etc/init/gunicorn-{host}.conf'
         .format(source_folder, host=host_name, user=user, site_name=site_name))

    # 最后，启动这两个服务
    sudo('service nginx reload && restart gunicorn-{host}'.format(host=host_name))


if __name__ == "__main__":
    pass
