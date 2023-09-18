from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

import logging

from ..mixins import TestUserAuthorizationMixin
from .models import AppUser
from .forms import UserCreateForm, UserUpdateForm

logger = logging.getLogger('main_log')


class UserListView(ListView):
    model = AppUser
    context_object_name = 'users'
    template_name = 'users/list.html'


class UserCreateView(SuccessMessageMixin, CreateView):
    form_class = UserCreateForm
    template_name = 'users/form.html'
    success_url = reverse_lazy('login')
    extra_context = {
        'title': 'Registration',
    }

    def form_valid(self, form):
        logger.debug('User is registered.')
        response = super().form_valid(form)
        messages.success(self.request, _('User is registered.'))
        return response

    def form_invalid(self, form):
        logger.error('User deletion error.')
        response = super().form_invalid(form)
        messages.error(self.request, _('User registration error.'))
        return response


class UserUpdateView(LoginRequiredMixin, TestUserAuthorizationMixin,
                     UpdateView):
    model = AppUser
    form_class = UserUpdateForm
    template_name = 'users/form.html'
    success_url = reverse_lazy('login')
    extra_context = {
        'title': 'Edit',
    }
    raise_exception = False

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


class UserDeleteView(LoginRequiredMixin, TestUserAuthorizationMixin,
                     DeleteView):
    model = AppUser
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users:list')

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
