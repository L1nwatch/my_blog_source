# 说明

此仓库保存的是我搭建自己博客的源码，本来一开始想跟着廖雪峰的教程搭的，后来发现还是用我自己比较熟悉的 Django 来搭吧。

## 参考资料

* [Django 搭建简易博客教程](http://wiki.jikexueyuan.com/project/django-set-up-blog/)
* [Bootstrap 中文文档](http://v3.bootcss.com/getting-started/#download)

## 开发环境

* macOSX 10.10.5
* Python 3.4
* virtualenv
* 部署服务器为 Ubuntu 系统

## 自动化部署方法

1. 进入 `/home/watch/sites/watch0.top` 目录，进行克隆操作，主要是为了获取 `deploy_tools` 文件夹下的自动化部署脚本
2. 执行命令，获取仓库中的所有文件，并放在文件夹 `source` 下：`git clone https://github.com/L1nwatch/my_blog_source.git source`
3. 进入自动化部署脚本目录：`/home/watch/sites/watch0.top/source/deploy_tools`
4. 执行命令，开始自动化部署操作：`fab deploy:host=watch@watch0.top:端口号 --password 你的密码`
5. ​


## 开发过程记录

* 安装好 virtualenv 后进入：`source virtual/bin/activate`
* 接着安装 `Django`：`pip install django`
* 然后创建博客工程：`./virtual/lib/python3.4/site-packages/django/bin/django-admin.py  startproject my_blog`
* 接着建立 `Django app`：`python manage.py startapp article`
* 数据库迁移：`python manage.py makemigrations` 以及 `python manage.py migrate`
* 超级管理员创建：`python manage.py createsuperuser`
* 应用 `bootstrap-admin` 进行美化，先 `pip` 进行安装，然后修改 `settings.py` 文件中：

```python
INSTALLED_APPS = [
    'bootstrap_admin',  # 一定要放在`django.contrib.admin`前面
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "articles"
]

BOOTSTRAP_ADMIN_SIDEBAR_MENU = True
```

* 安装 Markdown：`pip install markdown  #记得激活虚拟环境`
* 代码高亮：[找到自己喜欢的 CSS 文件](http://richleland.github.io/pygments-css/)，安装 `pip install pygments` 库，然后添加 link 到 html 中即可。
* 前端样式参考：[网址](http://www.purecss.org/layouts/blog/)，还有更全面的[不止是博客](http://www.purecss.org/layouts/)