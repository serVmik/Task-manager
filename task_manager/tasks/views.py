from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from task_manager.mixins import (
    HandleNoPermissionMixin,
    ModelFormMessagesMixin,
    ModelFormDeleteMessagesMixin,
    UserPassesTestOwnerMixin,
)

from task_manager.tasks.models import TaskModel
from task_manager.tasks.forms import TaskForm


class ListTasksView(ListView):
    model = TaskModel
    template_name = 'tasks/list.html'
    context_object_name = 'tasks'


class CreateTaskView(
    HandleNoPermissionMixin,
    ModelFormMessagesMixin,
    LoginRequiredMixin,
    CreateView,
):
    form_class = TaskForm
    template_name = 'tasks/form.html'
    success_url = reverse_lazy('tasks:create')
    extra_context = {
        'title': _('Create Task'),
    }
    valid_messages = _('Task successfully created')
    invalid_messaged = _('Error creating task')


class UpdateTaskView(
    HandleNoPermissionMixin,
    ModelFormMessagesMixin,
    LoginRequiredMixin,
    UpdateView,
):
    form_class = TaskForm
    template_name = 'tasks/form.html'
    success_url = reverse_lazy('tasks:update')
    extra_context = {
        'title': _('Update task')
    }
    valid_message = _('Task successfully updated')
    invalid_message = _('Task update error')


class DeleteTaskView(
    HandleNoPermissionMixin,
    ModelFormDeleteMessagesMixin,
    UserPassesTestOwnerMixin,
    DeleteView,
):
    model = TaskModel
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy('tasks:list')
    valid_message = _('Status successfully deleted')
    invalid_message = _('Error deleting status')
