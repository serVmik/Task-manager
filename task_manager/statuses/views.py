from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from task_manager.mixins import (
    HandleNoPermissionMixin,
    AddMessagesToFormSubmissionMixin,
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
    template_name = 'statuses/form.html'
    success_url = reverse_lazy('statuses:list')
    extra_context = {
        'title': _('Create status')
    }
    message_no_permission = _('Invalid action')
    success_message = _('Status successfully created')
    error_message = _('Error creating status')


class UpdateStatusView(
    HandleNoPermissionMixin,
    LoginRequiredMixin,
    AddMessagesToFormSubmissionMixin,
    UpdateView,
):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/form.html'
    success_url = reverse_lazy('statuses:list')
    extra_context = {
        'title': _('Edit status')
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
    protection_message = ''
    success_message = _('Status successfully deleted')
    error_message = _('Error deleting status')
    message_no_permission = _('Only the author can delete status')
