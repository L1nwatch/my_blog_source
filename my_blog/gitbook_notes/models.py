from django.db import models
from articles.models import BaseModel


class GitBook(BaseModel):
    book_name = models.CharField(max_length=100, blank=False)  # 书名, 不唯一
    href = models.CharField(max_length=255, blank=False, unique=True)  # URI, 唯一
    md_file_name = models.CharField(max_length=100, null=False)  # md 文件名, 不应该为空, 可以不唯一

    def __init__(self, *args, **kwargs):
        super(BaseModel, self).__init__(*args, **kwargs)

        # 书的分类, 默认值为 Others
        GitBook._meta.get_field('category').default = "Others"
