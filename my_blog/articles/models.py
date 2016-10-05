from django.db import models
from django.core.urlresolvers import reverse


# from django.contrib.sites.models import Site


class Tag(models.Model):
    tag_name = models.CharField(max_length=64)

    def __str__(self):
        return self.tag_name


class Article(models.Model):
    title = models.CharField(max_length=100, unique=True)  # 博客题目, 作为主键存在
    category = models.CharField(max_length=50, default="Others")  # 博客分类, 默认值为 Others
    tag = models.ManyToManyField(Tag, blank=True)  # 博客标签, 可为空
    date_time = models.DateTimeField(auto_now_add=True)  # 博客日期
    content = models.TextField(null=True, default=str())  # 博客文章正文

    def get_absolute_url(self):
        path = reverse('detail', kwargs={'id': self.id})
        return "http://127.0.0.1:8000{}".format(path)

    # python3使用__str__
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date_time']
