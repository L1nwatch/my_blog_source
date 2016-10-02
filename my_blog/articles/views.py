from django.shortcuts import render
from django.http import HttpResponse
from .models import Article


def home(request):
    post_list = Article.objects.all()  # 获取全部的Article对象
    return render(request, 'home.html', {'post_list': post_list})


def detail(request, my_args):
    db_data = Article.objects.all()[int(my_args)]
    message = "title = {}, category = {}, date_time = {}, content = {}".format(db_data.title, db_data.category,
                                                                               db_data.date_time,
                                                                               db_data.content)
    return HttpResponse(message)
