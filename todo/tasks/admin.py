from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'description_short', 'category', 'is_completed', 'created_at']
    list_filter = ['is_completed', 'category', 'created_at']
    search_fields = ['description']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['is_completed']

    @admin.display(description='Description')
    def description_short(self, obj):
        return obj.description[:50] + ('...' if len(obj.description) > 50 else '')
