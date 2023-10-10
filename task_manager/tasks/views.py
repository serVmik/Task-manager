from typing import Type

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django_filters.views import FilterView

from task_manager.mixins import (
    AddMessagesToFormSubmissionMixin,
    CheckAuthorshipTaskMixin,
    HandleNoPermissionMixin,
)
from task_manager.tasks.filters import TaskFilter
from task_manager.tasks.models import Task
from task_manager.tasks.forms import TaskForm


class ListTasksView(
    HandleNoPermissionMixin,
    LoginRequiredMixin,
    FilterView,
):
    model = Task
    template_name = 'tasks/list.html'
    context_object_name = 'tasks'
    filterset_class: Type[TaskFilter] = TaskFilter

    message_no_permission = _('You are not authorized')
    logger_no_permission = _('The action was taken by an unauthorized user')


class ShowTaskView(
    HandleNoPermissionMixin,
    LoginRequiredMixin,
    DetailView,
):
    model = Task
    template_name = 'tasks/show.html'
    context_object_name = 'task'
    message_no_permission = _('You are not authorized')
    logger_no_permission = _('The action was taken by an unauthorized user')


class CreateTaskView(
    HandleNoPermissionMixin,
    AddMessagesToFormSubmissionMixin,
    LoginRequiredMixin,
    CreateView,
):
    form_class = TaskForm
    template_name = 'tasks/form.html'
    success_url = reverse_lazy('tasks:list')
    extra_context = {
        'title': _('Create task'),
        'btn_name': _('Create'),
    }
    success_message = _('Task created successfully')
    error_message = _('Error adding task')
    message_no_permission = _('You are not authorized')
    logger_no_permission = _('The action was taken by an unauthorized user')

    def form_valid(self, form):
        """Add current user on author field Task model."""
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdateTaskView(
    HandleNoPermissionMixin,
    LoginRequiredMixin,
    AddMessagesToFormSubmissionMixin,
    UpdateView,
):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/form.html'
    success_url = reverse_lazy('tasks:list')
    extra_context = {
        'title': _('Changing a task'),
        'btn_name': _('Change')
    }
    success_message = _('The task was successfully modified')
    error_message = _('Task update error')
    message_no_permission = _('You are not authorized')
    logger_no_permission = _('The action was taken by an unauthorized user')


class DeleteTaskView(
    HandleNoPermissionMixin,
    CheckAuthorshipTaskMixin,
    AddMessagesToFormSubmissionMixin,
    DeleteView,
):
    model = Task
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy('tasks:list')
    extra_context = {
        'title': _('Deleting a task'),
        'btn_name': _('Yes, delete'),
    }
    success_message = _('The task was successfully deleted')
    message_no_permission = _('Only the author can delete task')
