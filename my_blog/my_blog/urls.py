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
2017.03.23 重构了部分搜索实现, 删除了通过 URL 来区分搜索类型的相关代码
"""
from django.conf.urls import url, include
from django.contrib import admin
import articles.views

urlpatterns = [
    url(r'^everything_is_happening_in_the_best_way/', admin.site.urls),
    url(r"^articles/", include("articles.urls")),
    url(r"^gitbook_notes/", include("gitbook_notes.urls")),
    url(r"^work_journal/", include("work_journal.urls")),
    url(r"^just_eating/", include("just_eating.urls")),
    url(r'^$', articles.views.home_view, name='home'),
    url(r"^search/$", articles.views.blog_search, name="search"),
]
