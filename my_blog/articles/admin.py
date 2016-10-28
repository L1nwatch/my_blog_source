from django.contrib import admin
from .models import Article
from .models import Tag


# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'create_time', "update_time")
    search_fields = ('title', 'category', 'tag', 'content')
    list_filter = ("update_time",)
    raw_id_fields = ('tag',)
    date_hierarchy = 'update_time'


admin.site.register(Article, ArticleAdmin)
admin.site.register(Tag)
