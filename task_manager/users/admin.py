from django.contrib import admin

from .models import UserModel
from ..labels.models import Label
from ..statuses.models import Status
from ..tasks.models import Task


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name',
                    'last_name', 'date_joined')
    list_display_links = ('id', 'username')
    search_fields = ('username', 'first_name', 'last_name',)
    list_filter = ('date_joined',)


class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status', 'author', 'executor', 'created_at')
    list_display_links = ('name', 'status', 'author', 'executor')
    search_fields = ('name',)
    list_filter = ('created_at', 'labels')


admin.site.register(UserModel, UserAdmin)
admin.site.register(Status)
admin.site.register(Label)
admin.site.register(Task, TaskAdmin)
