"""my_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URL conf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))


# 更新
2023.09.23 新增 AI 这个 APP
2021.10.08 新增 homepage 首页这个 APP
2019.03.21 新增 weixin 这个 APP
2017.06.30 新增 app_life_summary 这个 APP
2017.06.29 新增 timeline 这个 app
2017.06.21 新增一个自定义的 404 页面
2017.06.17 新增一个用于支持 Tag 搜索的 URL
2017.06.07 补充 google 认证网页
2017.03.28 新增 code_collect 这个 APP
2017.03.24 新增 tool hub 这个 APP
2017.03.23 重构了部分搜索实现, 删除了通过 URL 来区分搜索类型的相关代码
"""
# 标准库
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings

# 自己的模块
import articles.views
import homepage.views
import common_module.common_view

handler404 = 'common_module.common_view.handler404'
handler400 = 'common_module.common_view.handler404'

urlpatterns = [
    url(r'^everything_is_happening_in_the_best_way/', admin.site.urls),
    url(r"^articles/", include("articles.urls")),
    url(r"^gitbook_notes/", include("gitbook_notes.urls")),
    url(r"^work_journal/", include("work_journal.urls")),
    url(r"^just_eating/", include("just_eating.urls")),
    url(r'^(?P<search_type>[^/]+)/tag(?P<tag_name>[^/]+)/$', common_module.common_view.search_tag_view,
        name='search_tag'),
    url(r'^articles', articles.views.home_view, name='home'),
    url(r'^$', homepage.views.index_view, name='index'),
    url(r'^googlef0b96351a9e6fd45\.html$', articles.views.google_verify, name='google_verify'),
    url(r'^resume$', articles.views.resume, name='resume'),
    url(r'^cv$', articles.views.cv, name='cv'),
    url(r"^search/$", articles.views.blog_search, name="search"),
    url(r"^tool_hub/", include("toolhub.urls")),
    url(r"^code_collect/", include("code_collect.urls")),
    url(r"^timeline_app/", include("app_timeline.urls")),
    url(r"^life_summary_app/", include("app_life_summary.urls")),
    url(r"^weixin/", include("weixin.urls")),
    url(r"^ai/", include("artificial_intelligence.urls")),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns.append(url(r'^__debug__/', include(debug_toolbar.urls)))
