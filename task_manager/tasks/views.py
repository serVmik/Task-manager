import logging

from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from task_manager.mixins import (
    ModelFormMessagesMixin, HandleNoPermissionMixin, AuthorshipTaskCheckMixin,
)
from task_manager.tasks.models import Task
from task_manager.tasks.forms import TaskForm

logger = logging.getLogger('main_log')


class ListTasksView(
    HandleNoPermissionMixin,
    LoginRequiredMixin,
    ListView,
):
    model = Task
    template_name = 'tasks/list.html'
    context_object_name = 'tasks'
    message_no_permission = 'You are not authorized'
    logger_no_permission = 'The action was taken by an unauthorized user'


class CreateTaskView(
    HandleNoPermissionMixin,
    LoginRequiredMixin,
    ModelFormMessagesMixin,
    CreateView,
):
    form_class = TaskForm
    template_name = 'tasks/form.html'
    success_url = reverse_lazy('tasks:list')
    extra_context = {
        'title': _('Create Task'),
    }
    message_no_permission = 'You are not authorized'
    logger_no_permission = 'The action was taken by an unauthorized user'
    success_message = 'Task added successfully'
    error_message = 'Error adding task'

    def form_valid(self, form):
        """Add current user on author field Task model."""
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdateTaskView(
    HandleNoPermissionMixin,
    LoginRequiredMixin,
    ModelFormMessagesMixin,
    UpdateView,
):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/form.html'
    success_url = reverse_lazy('tasks:list')
    extra_context = {
        'title': _('Update task')
    }
    success_message = 'Task successfully updated'
    error_message = 'Task update error'
    message_no_permission = 'You are not authorized'
    logger_no_permission = 'The action was taken by an unauthorized user'


class DeleteTaskView(
    HandleNoPermissionMixin,
    AuthorshipTaskCheckMixin,
    ModelFormMessagesMixin,
    DeleteView,
):
    model = Task
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy('tasks:list')
    success_message = 'The task was successfully deleted'
    message_no_permission = 'Only the author can delete task'
