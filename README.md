# 说明

此仓库保存的是我搭建自己博客的源码，本来一开始想跟着廖雪峰的教程搭的，后来发现还是用我自己比较熟悉的 Django 来搭吧，结合网上的简易博客教程做了个模板，然后自己又编写了对应的功能测试和单元测试以便接下来的扩展，还有实现了自动化部署脚本，这样以后部署网站就方便多了。

## 开发环境

* macOSX 10.10.5
* Python 3.4
* virtualenv
* 部署服务器为 Ubuntu 系统，回头要搞个 docker (๑•̀ㅂ•́)و✧

## 界面如下

具体实现的效果可以到 [watch0.top](http://watch0.top) 上看

（2017-02-08 版本）的首页界面如图所示：

![2017-02-08首页截图](https://github.com/L1nwatch/my_blog_source/blob/master/2017-02-08%E9%A6%96%E9%A1%B5%E6%88%AA%E5%9B%BE.jpg?raw=true)

（2017-02-08 版本）的文章界面如图所示：

![2017-02-08文章截图](https://github.com/L1nwatch/my_blog_source/blob/master/2017-02-08%E6%96%87%E7%AB%A0%E7%95%8C%E9%9D%A2.jpg?raw=true)

（2017-02-15 版本）的日记界面如图所示：

![2017-02-15日记截图](https://github.com/L1nwatch/my_blog_source/blob/master/2017-02-15%E6%97%A5%E8%AE%B0%E9%A6%96%E9%A1%B5.jpg?raw=true)


### 更新情况

发现自己的 reamde 一点汇总的跟进信息都没有, 还是写一个吧

#### 2017.03.13

今天刚学了用 ngrok 进行内网穿透, 但是发现之前的 nginx 配置的 `proxy_pass` 跟这个有所冲突, 于是更新了一下 nginx conf 配置模板, 提供子域名 `temp.HOSTNAME` 作为内网穿透的入口, 端口号默认为 8080


## 自动化部署方法

1. 安装所需的软件，比如 nginx、git、Python、pip、virtualenv、fabric、supervisor 等，具体步骤：
   1. `sudo apt-get update`
   2. `sudo apt-get install nginx`
   3. `sudo apt-get install supervisor`
   4. `sudo apt-get install git`
   5. `sudo apt-get install python3`
   6. `sudo apt-get install python3-pip`
   7. `sudo apt-get install fabric`
   8. `sudo apt-get install python3-dev` 可能还需要安装 gcc，如果装 pycrypto 出错的话
   9. `sudo pip3 install virtualenv`
2. 进入 `/home/watch/sites/watch0.top` 目录，进行克隆操作，主要是为了获取 `deploy_tools` 文件夹下的自动化部署脚本【注意这里的 watch0.top，是能够访问到该台主机的域名】
3. 执行命令，获取仓库中的所有文件，并放在文件夹 `source` 下：`git clone https://github.com/L1nwatch/my_blog_source.git source`
4. 进入自动化部署脚本目录：`/home/watch/sites/watch0.top/source/deploy_tools`
5. 执行命令，开始自动化部署操作：`fab deploy:host=watch@watch0.top:端口号 --password=ssh密码 --sudo-password=sudo密码`。如果一切顺利，应该会有 `Done` 这个字样出现。【新版本的 fab 可能不需要 `--sudo-password=sudo密码`了，直接留下一个 `--password` 即可】
6. 部署期间需要输入用户名密码，这是 `work_journal` APP 需要的帐号密码，不需要使用到这个 APP 的话就随便输入一个吧
7. 访问首页，看是否正常。如果报出编码错误，则进行编码设置：`sudo vi /etc/default/locale`，这里使用的是：`LANG="zh_CN.utf8"\nLANGUAGE="zh_CN.utf8"\nLC_ALL="zh_CN.utf8"`
8. 【可选】创建超级管理员，使用命令 `python manage.py createsuperuser` 创建。
9. 修改 `my_blog/settings.py` 中的 `ARTICLES_GIT_REPOSITORY`，将其改为笔记的 git 仓库。然后点击首页上的 `手动更新笔记` 按钮，如果失败可以尝试重新运行自动化部署命令，然后再次点击 `手动更新笔记` 按钮。
10. 如果 `手动更新笔记` 还是失败，请确保 `locale -a` 中可以查看到 `zh_CN.utf8` (可以使用 `sudo locale-gen zh_CN.utf8` 安装)，然后设置默认 locale： `sudo vim /etc/default/locale` ，文件内容为：`LC_ALL="zh_CN.utf8"`
11. 回到首页，可以看到刚更新的文章了。
12. `2016.10.17` 更新：现在在自动化部署代码中会有自动更新数据库的定时任务在执行，所以不用手动更新数据库也行（定时任务默认每隔 2 个小时更新一次）


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

## 参考资料

* [Django 搭建简易博客教程](http://wiki.jikexueyuan.com/project/django-set-up-blog/)
* [Bootstrap 中文文档](http://v3.bootcss.com/getting-started/#download)
* Fab 文档参考，[中文版](http://fabric-chs.readthedocs.io/zh_CN/chs/index.html)，[英文版](http://www.fabfile.org/)
* 前端样式参考：[博客模板网址](http://www.purecss.org/layouts/blog/)，还有更全面的[不止是博客](http://www.purecss.org/layouts/)
* [supervisor 配置教程](https://3rgb.com/entry/daemon_control_autostart_with_supervisor)
* Python 探针(OneAPM) [blueware](http://blog.oneapm.com/apm-tech/202.html)
* [使用virtualenv在ubuntu上搭建python 3开发环境](https://my.oschina.net/xiaoiaozi/blog/129769)
* [如何更改Linux（Ubuntu）语言和编码设置](http://blog.csdn.net/bang987918/article/details/7711019)