from django.shortcuts import render
from django.http import HttpResponse, Http404

from .models import Article
import datetime


def home(request):
    post_list = Article.objects.all()  # 获取全部的Article对象
    return render(request, 'home.html', {'post_list': post_list})


def detail(request, article_number):
    try:
        db_data = Article.objects.get(id=article_number)
    except Article.DoesNotExist:
        raise Http404
    return render(request, "article.html", {"post": db_data})
