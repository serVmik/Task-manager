from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

import logging

from ..mixins import UserPassesTestOwnerMixin, NotLoginRequiredMixin
from .models import AppUser
from .forms import UserCreateForm, UserUpdateForm

logger = logging.getLogger('main_log')


class ListUsersView(ListView):
    model = AppUser
    context_object_name = 'users'
    template_name = 'users/list.html'


class CreateUserView(NotLoginRequiredMixin, CreateView):
    form_class = UserCreateForm
    template_name = 'users/form.html'
    success_url = reverse_lazy('login')
    extra_context = {
        'title': _('Registration'),
    }

    def form_valid(self, form):
        logger.debug('User is registered.')
        response = super().form_valid(form)
        messages.success(self.request, _('User is registered.'))
        return response

    def form_invalid(self, form):
        logger.error('User registration error.')
        response = super().form_invalid(form)
        messages.error(self.request, _('User registration error.'))
        return response


class UpdateUserView(UserPassesTestOwnerMixin, UpdateView):
    model = AppUser
    form_class = UserUpdateForm
    template_name = 'users/form.html'
    success_url = reverse_lazy('users:list')
    extra_context = {
        'title': _('Edit user'),
    }
    raise_exception = False

    def handle_no_permission(self):
        logger.error('Invalid action.')
        messages.error(self.request, _('Invalid action.'))
        return redirect(reverse_lazy('login'))

    def form_valid(self, form):
        logger.debug('User data updated.')
        response = super().form_valid(form)
        messages.success(self.request, _('User data updated.'))
        return response

    def form_invalid(self, form):
        logger.error('User update error.')
        response = super().form_invalid(form)
        messages.error(self.request, _('User update error.'))
        return response


class DeleteUserView(UserPassesTestOwnerMixin, DeleteView):
    model = AppUser
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users:list')

    def handle_no_permission(self):
        logger.error('Invalid action.')
        messages.error(self.request, _('Invalid action.'))
        return redirect(reverse_lazy('login'))

    def form_valid(self, form):
        logger.debug('User deleted.')
        response = super().form_valid(form)
        messages.success(self.request, _('User deleted.'))
        return response

    def form_invalid(self, form):
        logger.error('User deletion error.')
        response = super().form_invalid(form)
        messages.error(self.request, _('User deletion error.'))
        return response
