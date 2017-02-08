from django.db import models


class Journal(models.Model):
    title = models.CharField(max_length=100, blank=False, unique=True)  # 标题
    category = models.CharField(max_length=50, default="Sangfor")  # 博客分类, 默认值为 Sangfor
    content = models.TextField(null=True, default=str())  # 文章正文
    date = models.DateField(blank=False, unique=True)   # 日记的日期

    # python3使用__str__
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date']
