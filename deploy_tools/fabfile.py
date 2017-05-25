#!/bin/env python3
# -*- coding: utf-8 -*-
# version: Python3.X
""" 使用 Fabric 进行自动化部署

2017.05.25 补充发送邮件所需的相关部署操作
2017.03.05 更新 GitBook 的相关代码实线, 通过了全部测试, 另外也在 fab 中加入了对应的配置代码及文件
2017.02.10 添加配置文件读取, 将 git/username 等需要临时输入的信息用配置文件实现
2017.01.27 突然发现自己的 fab 不会去修改 DEBUG 选项, 现在改正了, 原来是那一句话被注释掉了
2016.10.19 修正一下 cron job 的问题, 现在可以实现每隔 5 分钟自动更新数据库了, 但是代码存在冗余, 可能以后要重构一下了
2016.10.17 增加一个定时任务, 每隔两个小时自动更新数据库
2016.10.06 本来是使用 gunicorn 模板来自动运行 gunicorn 的, 但是发现这样存在一个问题, 就是 gunicorn 的 locale 默认为空, 于是改为使用 supervisor
"""
import random
import string
import os
import sys
import re

# 兼容 Python 3 和 2 的导入
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run, sudo

__author__ = '__L1n__w@tch'

# 要把常量 REPO_URL 的值改成代码分享网站中你仓库的 URL
REPO_URL = "https://github.com/L1nwatch/my_blog_source.git"
USER_PASS_CONF = "user_pass.conf"
GITBOOKS_CONF = "gitbooks_git.conf"
SMTP_LOGIN_PASSWORD = ""


def deploy():
    """
    2016.10.04 根据之前的自动化部署代码进行更改, 这里要进行的几个操作包括:
        创建文件夹目录,获取最新版本代码,更新 settings 文件, 更新 Python 虚拟环境, 更新静态文件, 更新数据库, 设置 nginx 和 gunicorn
    """
    # env.host 的值是在命令行中指定的服务器地址，例如 watch0.top, env.user 的值是登录服务器时使用的用户名
    site_folder = "/home/{}/sites/{}".format(env.user, env.host)
    source_folder = os.path.join(site_folder, "source")
    virtualenv_folder = os.path.join(site_folder, "virtualenv")
    site_name = "my_blog"
    host_name = env.host
    user = env.user

    # 创建结构树
    _create_directory_structure_if_necessary(site_folder)

    # 更新代码
    _get_latest_source(source_folder)

    # 更新用户名密码的配置文件
    _user_pass_file_config()

    # 更新 gitbooks 链接
    _gitbooks_config(source_folder, site_name)

    # 更新 const 文件
    _update_const_file(source_folder, site_name)

    # 更新 setting 文件
    _update_settings(source_folder, site_name, host_name)

    # 更新虚拟环境以及所需的各个包
    _update_virtualenv(source_folder, virtualenv_folder)

    # 打包 static 文件
    _update_static_files(source_folder, virtualenv_folder, site_name)

    # 数据库迁移
    _update_database(source_folder, virtualenv_folder, site_name)

    # 设置服务器配置等
    _set_nginx_gunicorn_supervisor(source_folder, host_name, site_name, user)

    # 定时任务
    _set_cron_job(source_folder, virtualenv_folder, site_name, site_folder)


def _gitbooks_config(source_folder, site_name):
    print("[*] 即将读取 {} 下的 gitbooks 路径".format(GITBOOKS_CONF))

    # 读取文件内容
    with open(GITBOOKS_CONF, "r") as f:
        data = f.read()

    # 替换掉 constant.py 中的内容
    const_file_path = "{source_folder}/{site_name}/my_constant.py".format(source_folder=source_folder,
                                                                          site_name=site_name)

    # 通过 re 修改 const 文件
    with open(const_file_path, "r") as f:
        raw_git_data = f.read()
    raw_git_data = re.sub('const\.GITBOOK_CODES_REPOSITORY = \{[^}]*\}',
                          'const.GITBOOK_CODES_REPOSITORY = {}'.format(data), raw_git_data)

    with open(const_file_path, "w") as f:
        f.write(raw_git_data)

    print("[*] 成功将 {} 中的 gitbooks 路径更新到配置文件中".format(GITBOOKS_CONF))


def _create_config_file():
    """
    创建配置文件
    """
    global USER_PASS_CONF
    if not os.path.exists(USER_PASS_CONF):
        cp = configparser.ConfigParser()
        cp.add_section("journals_git")
        cp.add_section("articles_git")

        cp.set("journals_git", "username", "")
        cp.set("journals_git", "password", "")
        cp.set("articles_git", "address", "")

        with open(USER_PASS_CONF, "w") as f:
            cp.write(f)


def _user_pass_file_config():
    """
    判断一下 conf 文件是否存在指定内容, 如果是第一次运行的话得把 git 帐号密码保存进来
    """
    global USER_PASS_CONF, SMTP_LOGIN_PASSWORD

    # 确保配置文件存在
    _create_config_file()

    # 判断是否已经配置
    cp = configparser.ConfigParser()
    cp.read(USER_PASS_CONF)
    username, password = cp.get("journals_git", "username"), cp.get("journals_git", "password")
    articles_address = cp.get("articles_git", "address")

    while username == "" or password == "" or articles_address == "" or SMTP_LOGIN_PASSWORD == "":
        print("[+] 需要输入相关信息, 如不需要则随便打些字符即可")

        # 兼容 Python2.7
        if username == "":
            print("[+] 请输入 journals_git 的用户名: ")
            username = sys.stdin.readline().strip()
        if password == "":
            print("[+] 请输入 journals_git 的密码: ")
            password = sys.stdin.readline().strip()
        if articles_address == "":
            print("[+] 请输入 articles_git 的地址: ")
            articles_address = sys.stdin.readline().strip()
        if SMTP_LOGIN_PASSWORD == "":
            print("[+] 请输入 SMTP 登录密码(邮箱硬编码): ")
            SMTP_LOGIN_PASSWORD = sys.stdin.readline().strip()

        # 保存到配置文件中
        if username != "" and password != "" and articles_address != "":
            cp.set("journals_git", "username", username)
            cp.set("journals_git", "password", password)
            cp.set("articles_git", "address", articles_address)

            with open(USER_PASS_CONF, "w") as f:
                cp.write(f)

    print("[*] 成功读取文件 {} 的用户名和密码信息".format(USER_PASS_CONF))


def _update_const_file(source_folder, site_name):
    def __sub_callback(raw_string, user, pw):
        url = raw_string.group(1)
        new_url = "{0}//{username}:{password}@{1}".format(url.split("//")[0], url.split("//")[1],
                                                          username=user, password=pw)

        return 'const.JOURNALS_GIT_REPOSITORY = "{}"'.format(new_url)

    global USER_PASS_CONF
    const_file_path = "{source_folder}/{site_name}/my_constant.py".format(source_folder=source_folder,
                                                                          site_name=site_name)

    # 获取 username 和 password
    cp = configparser.ConfigParser()
    cp.read(USER_PASS_CONF)

    username, password = cp.get("journals_git", "username"), cp.get("journals_git", "password")
    articles_address = cp.get("articles_git", "address")

    # 通过 re 修改 const 文件
    with open(const_file_path, "r") as f:
        data = f.read()
    data = re.sub('const.JOURNALS_GIT_REPOSITORY = "(?P<git_url>.*)"',
                  lambda x: __sub_callback(x, username, password), data)
    data = re.sub('const.ARTICLES_GIT_REPOSITORY = ".*"',
                  'const.ARTICLES_GIT_REPOSITORY = "{}"'.format(articles_address), data)

    with open(const_file_path, "w") as f:
        f.write(data)


def _update_setting_to_conf_file(old_content, cron_job):
    """
    给配置文件添加对应的参数行
    # 2016.10.19 重构一下 _set_cron_job, 将其中关于修改文件内容的代码封装成函数
    :param old_content: 原来 crontab 已经存在的内容
    :param cron_job: 要添加到 crontab 的命令
    :return:
    """
    result_content_list = list()
    is_in_command_section = False
    has_set_cron_job = False
    for each_line in old_content:
        if is_in_command_section:
            # 已经存在 run_cron 设定, 那就不理了
            if "manage.py runcrons --force" in each_line.lower():
                if each_line.strip().lower() != cron_job:
                    each_line = cron_job
                has_set_cron_job = True
            # 到达该节的末尾了
            if each_line.strip() == "#":
                # 没设定的话就添加 run_cron 设定
                if not has_set_cron_job:
                    result_content_list.append(cron_job)
            result_content_list.append(each_line)
        else:
            result_content_list.append(each_line)

        # 设置 command 节标志位
        if "# m h dom mon dow user" in each_line.strip():
            is_in_command_section = True
        elif is_in_command_section and each_line.strip() == "#":
            is_in_command_section = False

    result_content_list = [each_line.strip() for each_line in result_content_list]
    result_content_list = [each_line + os.linesep for each_line in result_content_list]

    return result_content_list


def _set_cron_job(source_folder, virtualenv_folder, site_name, site_folder):
    """
    2016.10.19 仿照 __set_locale_for_supervisor 方法, 通过修改 /etc/crontab 文件来实现定时功能
    2016.10.17 添加第一个定时任务, 自动更新数据库
    :param source_folder: manage.py 所在的文件夹
    :param virtualenv_folder: 虚拟环境所在的文件夹
    :param site_name: 工程 app 名, 比如 my_blog
    :param site_folder: 网站所在的根目录, 即 source 的父目录
    :return:
    """
    # 大部分代码与 __set_locale_for_supervisor 类似, 这里是第 2 次使用, 如果使用了 3 次的话就要重构了
    temp_file1_name, temp_file2_name = "tEmP_conf1", "tEmP_conf2"
    temp_file1_path = os.path.join(source_folder, temp_file1_name)
    temp_file2_path = os.path.join(source_folder, temp_file2_name)

    # 直接用 with 语句打不开, 权限不够
    sudo("cd {}"
         " && cp /etc/crontab {}".format(source_folder, temp_file1_name))

    # 读取原来的 conf 文件到一个临时文件中
    with open(temp_file1_path, "r") as f:
        old_content = f.readlines()

    run_cron_job = ('*/5 * * * * root cd {source_folder}'
                    ' && {virtualenv_folder}/bin/python3 {site_name}/manage.py runcrons --force'
                    ' >> {site_folder}/log/cron_job.log'
                    .format(source_folder=source_folder, virtualenv_folder=virtualenv_folder,
                            site_name=site_name, site_folder=site_folder))

    result_content_list = _update_setting_to_conf_file(old_content, run_cron_job)

    with open(temp_file2_path, "w") as f:
        f.writelines(result_content_list)

    sudo("cd {}"
         " && cp {} /etc/crontab".format(source_folder, temp_file2_name))

    # 清除临时文件
    sudo("cd {}"
         " && rm {}"
         " && rm {}".format(source_folder, temp_file1_name, temp_file2_name))

    # 重启 cron 服务
    sudo("service cron restart")


def _create_directory_structure_if_necessary(site_folder):
    for sub_folder in ["virtualenv", "log"]:
        # run 的作用是在服务器中执行指定的 shell 命令
        # mkdir -p 是 mkdir 的一个有用变种，它有两个优势，其一是深入多个文件夹层级创建目录；其二，只在必要时创建目录。
        run("mkdir -p {}/{}".format(site_folder, sub_folder))


def _get_latest_source(source_folder):
    """
    执行 git 命令获取最新版本的代码
    # 2016.10.19 依旧得执行 2 次才能 git 到最新版本, 所以优化一下
    # 2016.10.06 觉得原先的版本老是没办法帮我得到最新的版本, 所以重新布置了一下
    :param source_folder: 代码所在的文件夹路径
    :return:
    """
    # exists 检查服务器中是否有指定的文件夹或文件。我们指定的是隐藏文件夹 .git，检查仓库是否已经克隆到文件夹中。
    if exists(source_folder + "/.git"):
        # 很多命令都以 cd 开头，其目的是设定当前工作目录。Fabric 没有状态记忆，所以下次运行 run 命令时不知道在哪个目录中
        # 在现有仓库中执行 git fetch 命令是从网络中拉取最新提交
        # run("cd {} && git fetch".format(source_folder))
        # Fabric 中的 local 函数在本地电脑中执行命令，这个函数其实是对 subprocess.Popen 的再包装。
        # 我们捕获 git log 命令的输出，获取本地仓库中当前提交的哈希值，这么做的结果是，服务器中代码将和本地检出的代码版本一致
        # current_commit = local("git log -n 1 --format=%H", capture=True)
        # 执行 git reset --hard 命令，切换到指定的提交。这个命令会撤销在服务器中对代码仓库所做的任何改动。
        # run("cd {} && git reset --hard {}".format(source_folder, current_commit))
        run("cd {} && git reset --hard".format(source_folder))
        run("cd {} && git pull".format(source_folder))

        # 再次确保获取最新版本
        run("cd {} && git reset --hard".format(source_folder))
        run("cd {} && git pull".format(source_folder))
    else:
        # 如果仓库不存在，就执行 git clone 命令克隆一份全新的源码。
        run("git clone {} {}".format(REPO_URL, source_folder))


def _update_settings(source_folder, site_name, host_name):
    """
    更新 settings 文件
    :param source_folder:
    :param site_name:
    :param host_name:
    :return: None
    """
    global SMTP_LOGIN_PASSWORD
    settings_path = source_folder + "/{site_name}/{site_name}/settings.py".format(site_name=site_name)

    # Fabric 提供的 sed 函数作用是在文本中替换字符串。这里把 DEBUG 的值由 True 改成 False
    # 关闭 django 调试模式
    sed(settings_path, "DEBUG = True", "DEBUG = False")
    sed(settings_path, 'DOMAIN = "localhost"', 'DOMAIN = "{}"'.format(host_name))
    # 修改发送邮件后台终端
    sed(settings_path, 'EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"',
        'EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"')
    # 修改 SMTP 登录密码
    sed(settings_path, "EMAIL_HOST_PASSWORD = ''", "EMAIL_HOST_PASSWORD = '{}'".format(SMTP_LOGIN_PASSWORD))
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


def __set_locale_for_supervisor(source_folder):
    """
    查找 supervisord.conf 中是否已经设定了 environment, 如果没有就添加该行设定
    :return:
    """
    temp_file1_name, temp_file2_name = "tEmP_conf1", "tEmP_conf2"
    temp_file1_path = os.path.join(source_folder, temp_file1_name)
    temp_file2_path = os.path.join(source_folder, temp_file2_name)
    sudo("cd {}"
         " && cp /etc/supervisor/supervisord.conf {}".format(source_folder, temp_file1_name))

    # 读取原来的 conf 文件到一个临时文件中
    with open(temp_file1_path, "r") as f:
        old_content = f.readlines()

    result_content_list = list()
    is_in_supervisord_section = False
    has_set_environment = False
    for each_line in old_content:
        if is_in_supervisord_section:
            # 已经存在 environment 设定, 那就不理了
            if each_line.startswith("environment"):
                has_set_environment = True
            # 到达该节的末尾了
            if each_line.startswith("; the below section must"):
                # 没设定的话就添加 locale 设定
                if not has_set_environment:
                    locale_setting = 'environment=LANG="zh_CN.utf8", LC_ALL="zh_CN.utf8", LC_LANG="zh_CN.utf8"'
                    result_content_list.append(locale_setting)
            result_content_list.append(each_line)
        else:
            result_content_list.append(each_line)

        # 设置 section 节标志位
        if each_line.startswith("[supervisord]"):
            is_in_supervisord_section = True
        elif each_line.startswith("; the below section must"):
            is_in_supervisord_section = False

    with open(temp_file2_path, "w") as f:
        result_content_list = [each_line.strip() for each_line in result_content_list]
        result_content_list = [each_line + os.linesep for each_line in result_content_list]
        f.writelines(result_content_list)

    sudo("cd {}"
         " && cp {} /etc/supervisor/supervisord.conf".format(source_folder, temp_file2_name))

    # 清除临时文件
    sudo("cd {}"
         " && rm {}"
         " && rm {}".format(source_folder, temp_file1_name, temp_file2_name))


def _set_nginx_gunicorn_supervisor(source_folder, host_name, site_name, user):
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
         ' | tee /etc/nginx/sites-available/{host}'.format(source_folder, host=host_name, user=user)
         )

    # 激活这个文件配置的虚拟主机
    sudo('ln -sf /etc/nginx/sites-available/{host} /etc/nginx/sites-enabled/{host}'.format(host=host_name))

    # 配置 supervisor 配置文件
    sudo('cd {}'
         ' && sed "s/HOST_NAME/{host}/g" deploy_tools/supervisor.template.conf'
         ' | sed "s/USER_NAME/{user}/g"'
         ' | sed "s/SITE_NAME/{site_name}/g"'
         ' | tee /etc/supervisor/conf.d/{host}.conf'
         .format(source_folder, host=host_name, user=user, site_name=site_name))

    # 给 supervisor 添加 locale 配置
    __set_locale_for_supervisor(source_folder)

    # 重启 nginx 服务以及 supervisor
    sudo('service nginx reload'
         ' && supervisorctl update'
         ' && supervisorctl restart gunicorn')


if __name__ == "__main__":
    pass
