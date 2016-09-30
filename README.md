# 说明

此仓库保存的是我搭建自己博客的源码，本来一开始想跟着廖雪峰的教程搭的，后来发现还是用我自己比较熟悉的 Django 来搭吧。

## 参考资料

* [Django 搭建简易博客教程](http://wiki.jikexueyuan.com/project/django-set-up-blog/)
* [Bootstrap 中文文档](http://v3.bootcss.com/getting-started/#download)

## 开发环境

* macOSX 10.10.5
* Python 3.4
* virtualenv

## 开发过程记录

安装好 virtualenv 后进入：`source virtual/bin/activate`

接着安装 `Django`：`pip install django`

然后创建博客工程：`./virtual/lib/python3.4/site-packages/django/bin/django-admin.py  startproject my_blog`

接着建立 `Django app`：`python manage.py startapp article`

