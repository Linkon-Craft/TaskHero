from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "due_date", "status", "priority")
    readonly_fields = ("due_date",)
    list_filter = ("priority", "due_date", "status")
    search_fields = ("title", "desc")