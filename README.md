# 说明

此仓库保存的是我搭建自己博客的源码，本来一开始想跟着廖雪峰的教程搭的，后来发现还是用我自己比较熟悉的 Django 来搭吧，结合网上的简易博客教程做了个模板，然后自己又编写了对应的功能测试和单元测试以便接下来的扩展，还有实现了自动化部署脚本，这样以后部署网站就方便多了。

## 开发环境

* macOSX 10.10.5
* Python 3.4
* virtualenv
* 部署服务器为 Ubuntu 系统，回头要搞个 docker (๑•̀ㅂ•́)و✧

## 界面如下

具体实现的效果可以到 [watch0.top](http://watch0.top) 上看

（2017-03-17 版本）的首页界面如图所示：

![2017-03-17首页截图](https://github.com/L1nwatch/my_blog_source/blob/master/2017-03-17%E9%A6%96%E9%A1%B5%E6%88%AA%E5%9B%BE.jpg?raw=true)

（2017-05-23 版本）的文章界面如图所示：

![2017-05-23-文章显示](https://github.com/L1nwatch/my_blog_source/blob/master/2017-05-23-%E6%96%87%E7%AB%A0%E6%98%BE%E7%A4%BA.jpg?raw=true)

（2017-03-23 版本）的日记界面如图所示：

![2017-03-23-日记首页](https://github.com/L1nwatch/my_blog_source/blob/master/2017-03-23-%E6%97%A5%E8%AE%B0%E9%A6%96%E9%A1%B5.jpg?raw=true)

（2017-06-29 版本）的时间线界面如图所示：

![2017-06-29-时间线首页](https://github.com/L1nwatch/my_blog_source/blob/master/2017-06-29-%E6%97%B6%E9%97%B4%E7%BA%BF%E9%A6%96%E9%A1%B5.jpg?raw=true)


### 更新情况

```shell
# Update
#	============================== 2023 Jan ==============================
2023.01.15
    更新 Python 版本到 3.9, 同时更新相关依赖库, 修正相关的自动化测试脚本
    更新部署脚本及部署说明
#	============================== 2018 Feb ==============================
2018.02.22
    新增了个凯撒加密到平台中
#	============================== 2017 Dec ==============================
2017.12.03
    (1)优化判断 IP 的方式
    (2)删除多余行, 提高代码覆盖率
    (3)功能测试改成用 Chrome 来进行
#	============================== 2017 Nov ==============================
2017.11.27
    硬编码 IP 也不行,有问题了
2017.11.26
    硬编码允许访问的 IP, 之前明明不需要这样做也可以的, 要不后面再加入域名解析流程吧
#	============================== 2017 Oct ==============================
2017.10.23
    修正搜索时带 ( 会导致 re 编译错误的 BUG
2017.10.14
    开始着手准备加密工具, 首先支持凯撒加密, 不过只是搬了基础的凯撒解密到前台
    新增一个 IP 访问限制的测试
#	============================== 2017 August ==============================
2017.08.29
    有些地方没有 IP 限制, 好尴尬, 补充一下
2017.08.26
    给日志加上 IP 访问限制
#	============================== 2017 July ==============================
2017.07.13
    为 timeline 以及 summary 添加 log
2017.07.09
    继续补充完善 summary 解析树的测试 + 测试通过(即现在不是硬编码 HTML 生成笔记了)
    修正一下 summary 在手机端和 iPad 端导航条会挡住笔记的 BUG
2017.07.07
    重构一下 event timeline 生成 html 的 方式
2017.07.02
    重构一下视图, 现在菜单栏是由代码生成的而不是硬编码的了
    编写测试, 继续改用代码编写 summary 而不是硬编码, 但是现在测试代码没写完, 模板逻辑倒是写好了, 视图函数还没写
#	============================== 2017 June ==============================
2017.06.30
    新增一个 life_summary APP, 专门用于记录自己的生活经历的
2017.06.29
    新增一个 timeline APP, 专门用于记录出行事件的
2017.06.27
    新增搜索界面中, 当标题太长的时候会让 Tag 换一行显示
2017.06.24
    补充 just_eating 的常量, 新增 sangfor 菜单, 为进入公司开始做准备
2017.06.23
    新增 ToolHub 中实验样本数计算工具的选项卡
2017.06.22
    补充完善 ToolHub 选项卡的测试
    再次修正吃饭菜单的 CSS, 确保 iPad/Mac/iPhone 的显示样式是我要的了
    再次修正归档页面的 CSS, 确保 iPad/Mac/iPhone 的样式, 话说好像得用 iPad 1024*768 的才对, 不是 768*1024= =
2017.06.21
    新增一个自定义的 404 页面
2017.06.17
    扩展 Tag 搜索函数, 现在不仅能够搜索 Articles 了, 还能够搜索 GitBook 的笔记了
2017.06.16
    完善手动更新按钮的测试代码
    给 GitBook 的笔记添加标签
    修正当文章标题过长时, 目录树加号与标题不在同一行的 Bug
2017.06.15
    通过了昨天编写的各个测试, 主要是实现了 ToolHub 里面的 STATIC html 映射
    修正一个失败但是 PyCharm 无法识别的测试案例
2017.06.14
    继续修改 CSS, 主要是统一 sidebar 样式 + 修改日记页面在不同设备的样式
2017.06.13
    继续修改各个地方 CSS, 修改文章目录树的 js 脚本, 主要是处理目录树显示的代码逻辑
    更改了一下文章界面的字体等 CSS
2017.06.11
    修复一下日志记录 deepcopy 导致的问题
2017.06.10
    添加日志记录的字段, 现在还会记录 UserAgent 等 HTTP 头的信息了
    添加控制变量, 这样可以控制要记录哪些 HTTP 头字段
    解决 request.META.items() 在遍历时会被修改的问题
2017.06.09
    修改吃饭菜单的样式, 现在可以根据 mac/iPad/iPhone 显示不同样式了
    专门针对 iPhone 修改菜单转盘的样式
2017.06.08
    由于之前的方式会导致 PyCharm 无法识别本常量脚本中的变量名, 因此重构了一下, 现在可以识别了, 不过常量脚本会有警告
    更改 tag/category 采用和 archives 一样的界面
    尝试本地进行部署, 根据错误修改部署脚本
2017.06.07
    更改 GitHub 图片地址转换工具右上角 DEMO 标签的显示, 现在不会每次复制都把 DEMO 也复制上了
    修改 ToolHub 首页时钟样式
    给搜索结果的标签添加 Tag 搜索功能 + 编写测试代码
    修正部署代码, 添加 www/non-www 的部署访问许可
2017.06.06
    再次修正, 现在可以确保正常内容、内联代码、代码块中的 XSS 攻击都正常显示了
    将所有有关 Archive 都合并到了同一个脚本之中, 另外补充有关 Tag 搜索的测试
2017.06.05
    继续完善有关 XSS 的测试以及代码实现, 使得在保证安全的前提下也可以正常显示 code, 但是目前只能解决反引号里面的代码显示
2017.06.04
    重构基类测试, 修改对应代码
    重构搜索结果数据结构
    添加有关搜索结果显示 Tag 的功能及测试
    完善更新笔记的代码, 现在更新笔记会顺便更新 Tag 了
2017.06.03
    修正笔记数的获取方式, 换了一个好像更高效的方法来统计
    继续重写代码逻辑, 避免数据库锁定以及发邮件卡顿的问题
    修改 log 打包后的名字, 主要是补充 0 位
2017.06.02
    优化排序代码 + 优化笔记数获取方式
#	============================== 2017 May ==============================
2017.05.30
    新增 IP 定位功能, 现在有 IP 访问可以识别出哪个国家哪个城市的
    完善发送邮件的内容, 邮件标题加上访问 IP 的地理信息
    更改了邮件发送标题, 重构了一下各个模块
2017.05.29
    继续补充部署代码的测试文件, 并且完善 email 各个字段的部署操作
2017.05.28
    补充发送邮件的相关测试, 将 log_file_deal 的测试也加入到 django test all 里面
    继续重构部署代码, 主要是重构更新配置文件这一部分, 并且补充更新配置文件的相关测试
    为部署代码添加邮件发送相关的配置信息(之前是硬编码的)
2017.05.27
    尝试重构部署代码, 主要是与用户交互保存配置信息的这一部分
    补充用户交互配置的相关测试代码
2017.05.26
    修正一下发送邮件的操作不会记录日志的 BUG
    更改硬编码的邮箱地址, 原来是 qq 邮箱现在改成 qq 企业邮箱
    完善一下部署过程中设置发送邮件相关信息的部署操作
    修复相关 BUG, 现在终于可以自动发邮件过来了
    补充 log 装饰器的测试
2017.05.25
    修改 ToolHub 样式, 现在对应界面的按钮会变绿
    新增发送邮件的相关操作, 现在每遇到不认识的 IP 地址都会发送到自己的邮箱当中, 目前版本存在大量代码硬编码, 需要重构
    邮件发送改为多线程, 避免邮件发送失败时导致前端也显示不了了
2017.05.24
    对 md 文件存在不安全因素这种情况增加相应的测试与代码过滤
2017.05.23
    继续修改文章显示界面左边目录树的样式, 现在可以支持子目录并且当目录比较小时会自动展开
2017.05.22
    修改文章显示界面左边目录树的样式, 虽然感觉好像只有我会觉得好看= =
2017.05.21
    实现搜索结果按照点击次数排序的功能, 另外重构了一下测试代码
2017.05.20
    完善 ToolHub 中选择按钮的功能, 现在会选择全部并且复制到剪切板, 而不仅仅是选择全部的功能了
    新增服务器打包日志的功能代码
2017.05.15
    新增转盘页面的选择地点功能, 新增相关测试
2017.05.01
    完善一下验证更新时间的前台交互代码
#	============================== 2017 April ==============================
2017.04.30
    重构及完善 GitBook title 相关的格式、测试、代码实现等
    完善 GitBook CONF 配置文件, 新增书名信息, 以及 is_valid_git_address 判断函数等
    修正测试, 加入到 django 测试框架中, 补充没写的 test_do_nothing_when_exist
2017.04.29
    完善一下 log 装饰器，补充元信息以及强制关键字参数
2017.04.05
    给 selenium 添加 proxy, 以后不用太担心翻墙失败的问题了
2017.04.04
    新增有关凯撒密码的 toolhub 超链接
2017.04.03
    重构一下创建测试数据的代码, 将其分离出来单独作为一个基类了
#	============================== 2017 March ==============================
2017.03.31
    修正一下 code 搜索出来 gitbook 和 journal 链接不正确的问题
2017.03.30
    全部测试通过了, 现在可以进行 Code 搜索了
    把更新笔记的函数执行也记录进日志里
2017.03.28
    新增 about me 页面, 是由 Pages 转换成的, 另外修改 about me 测试
    开始新增 code_collect 这个 APP, 用于搜索所有笔记中的代码块
2017.03.26
    添加搜索时的合法性校验
2017.03.25
    更新 Toolhub 的内容, 包括新增 Textarea 的 form、更改 ajax 为 post 请求、修改 toolhub 首页、把输入框和输出框分离等
    修正一下更新笔记时会删除过多后缀的问题
    改了一下搜索结果排序的逻辑代码
2017.03.24
    新增一个 APP: ToolHub, 里面存放自己的各种小工具, 目前只存放了 GitHub 图片地址转换器
2017.03.23
    重构了部分搜索实现, 删除了通过 URL 来区分搜索类型的相关代码, 更新一下 readme
    实现了搜索结果进行排序
2017.03.22
    添加一个转盘网页, 实现随机选择备选菜单的功能, 同时实现页面随着设备大小而采用不同的 CSS
2017.03.18
    修正不友好 md 文件的解析问题, 发现不是 md 不友好, 而是自己的代码不够健壮, 尴尬了(〒︿〒)
    重构 form 之后判断 form valid 的小 bug 也被修复了, 删除了之前自定义的 form valid 判断
2017.03.17
    去掉所有页面 search_choice 的显示样式
    修正 focus 的 bug, 现在单击完下拉菜单就可以自动 focus 到 input 框了
    针对某个不友好的 md 文件解析出错进行了一系列修正与完善
2017.03.16 
    给首页添加搜索选项基本完成了, 但是这个版本不太满意, 主要是样式上的不满意, 所以会尝试下一个版本。
    首页的搜索样式已经改好了, 但是分页多出来的 select 框还没来得及去掉
2017.03.14 
    修正首页, 将 About me 换成图标放在右下角, 另外开始修改搜索框, 更改了前端样式, 以便接下来扩展为搜索特定区域
2017.03.13
    今天刚学了用 ngrok 进行内网穿透, 但是发现之前的 nginx 配置的 proxy_pass 跟这个有所冲突, 于是更新了一下 nginx conf 配置模板, 提供子域名 temp.HOSTNAME 作为内网穿透的入口, 端口号默认为 8080
```

## 自动化部署方法

1. 代码下载到服务器
```shell
# 创建指定文件夹, /home/用户名/sites/域名, 【注意这里的 watch0.top，是能够访问到该台主机的域名】
mkdir /home/watch/sites/watch0.top
# git clone 代码到本地
git clone https://github.com/L1nwatch/my_blog_source.git source
```
2. 安装所需的软件，比如 nginx、git、Python、pip、virtualenv、fabric、supervisor 等
   * 手动安装：
```shell
sudo apt-get update
sudo apt-get install nginx
sudo apt-get install supervisor
sudo apt-get install git
sudo apt-get install python3.9
sudo apt-get install python3.9-pip
sudo apt-get install fabric
# 可能还需要安装 gcc，如果装 pycrypto 出错的话
sudo apt-get install python3-dev 
sudo pip3 install virtualenv
```
   * 脚本安装：`bash /home/watch/sites/watch0.top/source/deploy_tools/deploy.sh`
3. 进入自动化部署脚本目录：`/home/watch/sites/watch0.top/source/deploy_tools`
4. 执行命令，开始自动化部署操作：`fab deploy:host=watch@watch0.top:端口号 --password=ssh密码 --sudo-password=sudo密码`。如果一切顺利，应该会有 `Done` 这个字样出现。【新版本的 fab 可能不需要 `--sudo-password=sudo密码`了，直接留下一个 `--password` 即可】
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