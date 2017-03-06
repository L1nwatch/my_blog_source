from django.contrib import admin

from gitbook_notes.models import GitBook


class GitBookAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'book_name', "href", "md_file_name")
    search_fields = ('title', 'category', 'book_name', 'md_file_name', "content")
    list_filter = ("book_name",)


admin.site.register(GitBook, GitBookAdmin)
