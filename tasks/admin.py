from django.contrib import admin
from .models import Task
from .models import Role, UserProfile

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'assignee', 'creator', 'completed', 'created_at')
    list_filter = ('completed', 'created_at', 'assignee')
    search_fields = ('title', 'description')

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name',)
    filter_horizontal = ('permissions',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
