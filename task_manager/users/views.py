from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

import logging

from ..mixins import TestUserAuthorizationMixin
from .models import AppUser
from .forms import UserCreateForm, UserUpdateForm

logger = logging.getLogger('__name__')


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
    success_message = _('New user successfully registered')
    if success_message:
        logger.debug('New user successfully registered. id_username = ')
    else:
        logger.error('User registration error.')


class UserUpdateView(LoginRequiredMixin, TestUserAuthorizationMixin, UpdateView):
    model = AppUser
    form_class = UserUpdateForm
    template_name = 'users/form.html'
    success_url = reverse_lazy('login')
    extra_context = {
        'title': 'Edit',
    }


class UserDeleteView(LoginRequiredMixin, TestUserAuthorizationMixin, DeleteView):
    model = AppUser
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users:list')
