from django.db import models
from articles.models import BaseModel


class Journal(BaseModel):
    date = models.DateField(blank=False, unique=True)  # 日记的日期

    def __init__(self, *args, **kwargs):
        super(BaseModel, self).__init__(*args, **kwargs)

        # 日记分类, 默认值为 Sangfor
        Journal._meta.get_field('category').default = "Sangfor"

    class Meta:
        ordering = ['-date']
