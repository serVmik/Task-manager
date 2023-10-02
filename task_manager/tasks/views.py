import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from task_manager.tasks.models import Task
from task_manager.tasks.forms import TaskForm

logger = logging.getLogger('main_log')


class ListTasksView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/list.html'
    context_object_name = 'tasks'

    def handle_no_permission(self):
        logger.debug(_('The action was taken by an unauthorized user'))
        messages.error(self.request, _('You are not authorized'))
        return redirect(reverse_lazy('login'))


class CreateTaskView(LoginRequiredMixin, CreateView):
    form_class = TaskForm
    template_name = 'tasks/form.html'
    success_url = reverse_lazy('tasks:list')
    extra_context = {
        'title': _('Create Task'),
    }

    def handle_no_permission(self):
        logger.debug(_('The action was taken by an unauthorized user'))
        messages.error(self.request, _('You are not authorized'))
        return redirect(reverse_lazy('login'))

    def form_valid(self, form):
        form.instance.author = self.request.user
        logger.error(_('Task added successfully'))
        messages.success(self.request, _('Task added successfully'))
        return super().form_valid(form)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        logger.error(_('Error adding task'))
        messages.error(self.request, _('Error adding task'))
        return response


class UpdateTaskView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/form.html'
    success_url = reverse_lazy('tasks:list')
    extra_context = {
        'title': _('Update task')
    }

    def handle_no_permission(self):
        logger.debug(_('The action was taken by an unauthorized user'))
        messages.error(self.request, _('You are not authorized'))
        return redirect(reverse_lazy('login'))

    def form_valid(self, form):
        form.instance.author = self.request.user
        logger.error(_('Task successfully updated'))
        messages.success(self.request, _('Task successfully updated'))
        return super().form_valid(form)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        logger.error(_('Task update error'))
        messages.error(self.request, _('Task update error'))
        return response


class DeleteTaskView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy('tasks:list')

    def handle_no_permission(self):
        logger.error(_('Only the owner can delete user'))
        messages.error(self.request, _('Only the owner can delete user'))
        return redirect(reverse_lazy('login'))

    def authorship_test(self):
        author = self.get_object().author.pk
        current_user = self.request.user.pk
        return author == current_user

    def get_test_func(self):
        return self.authorship_test

    def form_valid(self, form):
        response = super().form_valid(form)
        logger.debug(_('The task was successfully deleted'))
        messages.success(self.request, _('The task was successfully deleted'))
        return response
