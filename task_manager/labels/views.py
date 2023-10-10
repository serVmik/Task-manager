from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from .models import Label
from .forms import LabelForm
from ..mixins import (
    AddMessagesToFormSubmissionMixin,
    HandleNoPermissionMixin,
    RedirectForModelObjectDeleteErrorMixin
)


class ListLabelsView(
    HandleNoPermissionMixin,
    LoginRequiredMixin,
    ListView,
):
    model = Label
    template_name = 'labels/list.html'
    context_object_name = 'labels'


class CreateLabelView(
    HandleNoPermissionMixin,
    LoginRequiredMixin,
    AddMessagesToFormSubmissionMixin,
    CreateView,
):
    form_class = LabelForm
    template_name = 'form.html'
    success_url = reverse_lazy('labels:list')
    extra_context = {
        'title': _('Create label'),
        'btn_name': _('Create'),
    }

    success_message = _('Label created successfully')
    error_message = _('Error creating label')


class UpdateLabelView(
    HandleNoPermissionMixin,
    LoginRequiredMixin,
    AddMessagesToFormSubmissionMixin,
    UpdateView,
):
    model = Label
    form_class = LabelForm
    template_name = 'form.html'
    success_url = reverse_lazy('labels:list')
    extra_context = {
        'title': _('Edit label'),
        'btn_name': _('Edit'),
    }

    success_message = _('Label updated successfully')
    error_message = _('Label update error')


class DeleteLabelView(
    HandleNoPermissionMixin,
    LoginRequiredMixin,
    RedirectForModelObjectDeleteErrorMixin,
    AddMessagesToFormSubmissionMixin,
    DeleteView,
):
    model = Label
    template_name = 'labels/delete.html'
    success_url = reverse_lazy('labels:list')
    protected_redirect_url = reverse_lazy('labels:list')
    extra_context = {
        'title': _('Delete label'),
        'btn_name': _('Yes, delete'),
    }

    success_message = _('Label deleted successfully')
    error_message = _('Label delete error')
    protected_message = _('Cannot delete label because it is in use')
