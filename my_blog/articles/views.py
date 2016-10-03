from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Article

HOME_PAGE_ARTICLES_NUMBERS = 2


def home(request):
    articles = Article.objects.all()  # 获取全部的Article对象
    paginator = Paginator(articles, HOME_PAGE_ARTICLES_NUMBERS)  # 每页显示 HOME_PAGE_ARTICLES_NUMBERS 篇
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    # except EmptyPage: # 没用到, 不知道干啥的
    #     post_list = paginator.paginator(paginator.num_pages)
    return render(request, 'home.html', {'post_list': post_list})


def detail(request, id):
    try:
        db_data = Article.objects.get(id=str(id))
        tags = db_data.tag.all()
    except Article.DoesNotExist:
        raise Http404
    return render(request, "article.html", {"post": db_data, "tags": tags})


def archives(request):
    try:
        post_list = Article.objects.all()
    except Article.DoesNotExist:
        raise Http404
    return render(request, 'archives.html', {'post_list': post_list,
                                             'error': False})


def about_me(request):
    return render(request, 'aboutme.html')


def search_tag(request, tag):
    try:
        post_list = Article.objects.filter(category__iexact=tag)  # contains
    except Article.DoesNotExist:
        raise Http404
    return render(request, 'tag.html', {'post_list': post_list})


def blog_search(request):
    if 's' in request.GET:
        s = request.GET['s']
        if not s:
            return render(request, 'home.html')
        else:
            post_list = Article.objects.filter(title__icontains=s)
            if len(post_list) == 0:
                return render(request, 'archives.html', {'post_list': post_list,
                                                         'error': True})
            else:
                return render(request, 'archives.html', {'post_list': post_list,
                                                         'error': False})
    return redirect('/')
