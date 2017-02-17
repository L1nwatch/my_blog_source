from django.db import models
from django.core.urlresolvers import reverse


class BaseModel(models.Model):
    title = models.CharField(max_length=100, blank=False, unique=True)  # 文章或日记的题目
    category = models.CharField(max_length=50)  # 博客分类
    content = models.TextField(null=True, default=str())  # 博客文章正文

    # python3使用__str__
    def __str__(self):
        return self.title


class Tag(models.Model):
    tag_name = models.CharField(max_length=64)

    def __str__(self):
        return self.tag_name


class Article(BaseModel):
    tag = models.ManyToManyField(Tag, blank=True)  # 博客标签, 可为空
    create_time = models.DateTimeField(auto_now_add=True)  # 文章创建日期
    update_time = models.DateTimeField(auto_now_add=True)  # 文章更新日期

    def __init__(self, *args, **kwargs):
        super(Article, self).__init__(*args, **kwargs)

        # 博客分类, 默认值为 Others
        Article._meta.get_field('category').default = "Others"

    def get_absolute_url(self):
        path = reverse('detail', kwargs={'article_id': self.id})
        return "http://127.0.0.1:8000{}".format(path)

    class Meta:
        ordering = ['-update_time']
