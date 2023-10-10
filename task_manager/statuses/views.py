from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from task_manager.mixins import (
    AddMessagesToFormSubmissionMixin,
    HandleNoPermissionMixin,
)
from task_manager.statuses.forms import StatusForm
from task_manager.statuses.models import Status


class ListStatusesView(
    HandleNoPermissionMixin,
    LoginRequiredMixin,
    ListView,
):
    model = Status
    context_object_name = 'statuses'
    template_name = 'statuses/list.html'


class CreateStatusView(
    HandleNoPermissionMixin,
    LoginRequiredMixin,
    AddMessagesToFormSubmissionMixin,
    CreateView,
):
    form_class = StatusForm
    template_name = 'form.html'
    success_url = reverse_lazy('statuses:list')
    extra_context = {
        'title': _('Create status'),
        'btn_name': _('Create'),
    }

    success_message = _('Status successfully created')
    error_message = _('Error creating status')
    message_no_permission = _('Invalid action')


class UpdateStatusView(
    HandleNoPermissionMixin,
    LoginRequiredMixin,
    AddMessagesToFormSubmissionMixin,
    UpdateView,
):
    model = Status
    form_class = StatusForm
    template_name = 'form.html'
    success_url = reverse_lazy('statuses:list')
    extra_context = {
        'title': _('Edit status'),
        'btn_name': _('Edit'),
    }

    success_message = _('Status updated successfully')
    error_message = _('Status update error')


class DeleteStatusView(
    HandleNoPermissionMixin,
    LoginRequiredMixin,
    AddMessagesToFormSubmissionMixin,
    DeleteView
):
    model = Status
    template_name = 'statuses/delete.html'
    success_url = reverse_lazy('statuses:list')
    extra_context = {
        'title': _('Delete status'),
        'btn_name': _('Yes, delete'),
    }

    success_message = _('Status successfully deleted')
    error_message = _('Error deleting status')
    message_no_permission = _('Only the author can delete status')
