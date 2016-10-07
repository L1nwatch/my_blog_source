# 说明

此仓库保存的是我搭建自己博客的源码，本来一开始想跟着廖雪峰的教程搭的，后来发现还是用我自己比较熟悉的 Django 来搭吧，结合网上的简易博客教程做了个模板，然后自己又编写了对应的功能测试和单元测试以便接下来的扩展，还有实现了自动化部署脚本，这样以后部署网站就方便多了。

## 参考资料

* [Django 搭建简易博客教程](http://wiki.jikexueyuan.com/project/django-set-up-blog/)
* [Bootstrap 中文文档](http://v3.bootcss.com/getting-started/#download)
* Fab 文档参考，[中文版](http://fabric-chs.readthedocs.io/zh_CN/chs/index.html)，[英文版](http://www.fabfile.org/)
* 前端样式参考：[博客模板网址](http://www.purecss.org/layouts/blog/)，还有更全面的[不止是博客](http://www.purecss.org/layouts/)
* [supervisor 配置教程](https://3rgb.com/entry/daemon_control_autostart_with_supervisor)
* Python 探针(OneAPM) [blueware](http://blog.oneapm.com/apm-tech/202.html)

## 开发环境

* macOSX 10.10.5
* Python 3.4
* virtualenv
* 部署服务器为 Ubuntu 系统

## 自动化部署方法

1. 安装所需的软件，比如 nginx、git、Python、pip、virtualenv、fabric、supervisor 等：`sudo apt-get install nginx supervisor git python3 python3-pip fabric`

2. 进入 `/home/watch/sites/watch0.top` 目录，进行克隆操作，主要是为了获取 `deploy_tools` 文件夹下的自动化部署脚本

3. 执行命令，获取仓库中的所有文件，并放在文件夹 `source` 下：`git clone https://github.com/L1nwatch/my_blog_source.git source`

4. 进入自动化部署脚本目录：`/home/watch/sites/watch0.top/source/deploy_tools`

5. 执行命令，开始自动化部署操作：`fab deploy:host=watch@watch0.top:端口号 --password=ssh密码 --sudo-password=sudo密码`。如果一切顺利，应该会有 `Done` 这个字样出现。

6. 访问首页，看是否正常。【可选】接着创建超级管理员，使用命令 `python manage.py createsuperuser` 创建。

7. 修改 `my_blog/settings.py` 中的 `TEST_GIT_REPOSITORY`，将其改为笔记的 git 仓库。然后点击首页上的 `手动更新笔记` 按钮，如果失败可以尝试重新运行自动化部署命令，然后再次点击 `手动更新笔记` 按钮。

8. 如果 `手动更新笔记` 还是失败，请确保 `locale -a` 中可以查看到 `zh_CN.utf8` (可以使用 `sudo locale-gen zh_CN.utf8` 安装)，然后设置默认 locale： `sudo vim /etc/default/locale` ，文件内容为：`LC_ALL="zh_CN.utf8"`

9. 回到首页，可以看到刚更新的文章了。（2016.10.06 版本）的界面如图所示：

   ![20161006界面](https://github.com/L1nwatch/my_blog_source/blob/master/2016-10-06-%E7%BD%91%E7%AB%99%E6%88%AA%E5%9B%BE.png?raw=true)


## 开发过程记录

* 安装好 virtualenv 后进入：`source virtual/bin/activate`，退出命令：`deactivate`
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