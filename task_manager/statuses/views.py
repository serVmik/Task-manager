from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from task_manager.mixins import (
    HandleNoPermissionMixin,
    ModelFormMessagesMixin,
    ModelFormDeleteMessagesMixin,
)

from task_manager.statuses.forms import StatusForm
from task_manager.statuses.models import Status


class ListStatusesView(HandleNoPermissionMixin, LoginRequiredMixin, ListView):
    model = Status
    context_object_name = 'statuses'
    template_name = 'statuses/list.html'


class CreateStatusView(
    ModelFormMessagesMixin,
    HandleNoPermissionMixin,
    LoginRequiredMixin,
    CreateView,
):
    form_class = StatusForm
    template_name = 'statuses/form.html'
    success_url = reverse_lazy('statuses:list')
    extra_context = {
        'title': _('Create status')
    }
    valid_message = _('Status successfully created')
    invalid_message = _('Error creating status')


class UpdateStatusView(
    ModelFormMessagesMixin,
    HandleNoPermissionMixin,
    LoginRequiredMixin,
    UpdateView,
):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/form.html'
    success_url = reverse_lazy('statuses:list')
    extra_context = {
        'title': _('Edit status')
    }
    valid_message = _('Status updated successfully')
    invalid_message = _('Status update error')


class DeleteStatusView(
    ModelFormDeleteMessagesMixin,
    HandleNoPermissionMixin,
    LoginRequiredMixin,
    DeleteView
):
    model = Status
    template_name = 'statuses/delete.html'
    success_url = reverse_lazy('statuses:list')
    valid_message = _('Status successfully deleted')
    invalid_message = _('Error deleting status')
