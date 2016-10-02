from django.shortcuts import render
from django.http import HttpResponse
from .models import Article


def home(request):
    return HttpResponse("Hello World, Django")


def detail(request, my_args):
    db_data = Article.objects.all()[int(my_args)]
    message = "title = {}, category = {}, date_time = {}, content = {}".format(db_data.title, db_data.category,
                                                                               db_data.date_time,
                                                                               db_data.content)
    return HttpResponse(message)
