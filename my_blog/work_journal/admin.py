from django.contrib import admin
from .models import Journal


# Register your models here.
class JournalAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'content',)
    search_fields = ('title', 'category', 'content')
    list_filter = ("title",)


admin.site.register(Journal, JournalAdmin)
