from django.contrib import admin
from code_collect.models import CodeCollect


# Register your models here.
class CodeCollectAdmin(admin.ModelAdmin):
    list_display = ('note', 'code_type')
    search_fields = ('code_type',)
    list_filter = ("code_type",)


admin.site.register(CodeCollect, CodeCollectAdmin)
