from django.contrib import admin
from .models import Journal


# Register your models here.
class JournalAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'content', "date")
    search_fields = ('title', 'category', 'content', "date")
    list_filter = ("date",)
    date_hierarchy = 'date'


admin.site.register(Journal, JournalAdmin)
