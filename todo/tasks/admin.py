from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'title_short', 'category', 'is_completed', 'created_at']
    list_filter = ['is_completed', 'category', 'created_at']
    search_fields = ['title']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['is_completed']

    @admin.display(description='Title')
    def title_short(self, obj):
        return obj.title[:50] + ('...' if len(obj.title) > 50 else '')
