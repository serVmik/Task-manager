from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

import logging

from task_manager.statuses.forms import StatusForm
from task_manager.statuses.models import Status

logger = logging.getLogger('main_log')


class CreateStatusView(LoginRequiredMixin, CreateView):
    form_class = StatusForm
    template_name = 'statuses/form.html'
    success_url = reverse_lazy('statuses:list')
    extra_context = {
        'title': _('Create status')
    }

    def handle_no_permission(self):
        messages.error(self.request, _('Invalid action.'))
        return redirect(reverse_lazy('statuses:list'))

    def form_valid(self, form):
        response = super().form_valid(form)
        logger.debug('Status successfully created')
        messages.success(self.request, _('Status successfully created'))
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        logger.error('Error creating status')
        messages.error(self.request, _('Error creating status'))
        return response


class ListStatusesView(ListView):
    model = Status
    context_object_name = 'statuses'
    template_name = 'statuses/list.html'


class UpdateStatusView(UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/form.html'
    success_url = reverse_lazy('statuses:list')
    extra_context = {
        'title': _('Edit status')
    }

    def form_valid(self, form):
        response = super().form_valid(form)
        logger.debug('Status updated successfully')
        messages.success(self.request, _('Status updated successfully'))
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        logger.error('Status update error')
        messages.error(self.request, _('Status update error'))
        return response


class DeleteStatusView(LoginRequiredMixin, DeleteView):
    model = Status
    template_name = 'statuses/delete.html'
    success_url = reverse_lazy('statuses:list')

    def handle_no_permission(self):
        messages.error(self.request, _('Invalid action.'))
        return redirect(reverse_lazy('statuses:list'))

    def form_valid(self, form):
        response = super().form_valid(form)
        logger.debug('Status successfully deleted')
        messages.success(self.request, _('Status successfully deleted'))
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        logger.error('Error deleting status')
        messages.error(self.request, _('Error deleting status'))
        return response
