from django.contrib import admin
from .models import Log

@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'user', 'priority', 'log_date', 'created_at']
    list_filter = ['priority', 'log_date', 'created_at']
    search_fields = ['title', 'description', 'user__username']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'log_date'
    ordering = ['-log_date', '-created_at']
