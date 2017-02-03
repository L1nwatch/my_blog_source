from django.db import models


class Journal(models.Model):
    title = models.CharField(max_length=100, blank=False, unique=True)  # 标题
    category = models.CharField(max_length=50, default="Others")  # 博客分类, 默认值为 Others
    content = models.TextField(null=True, default=str())  # 文章正文

    # python3使用__str__
    def __str__(self):
        return self.title
