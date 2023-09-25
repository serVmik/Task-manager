from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from ..mixins import (
    HandleNoPermissionMixin,
    UserPassesTestOwnerMixin,
    ModelFormMessagesMixin,
    ModelFormDeleteMessagesMixin,
    NotLoginRequiredMixin,
)
from .models import AppUser
from .forms import UserCreateForm, UserUpdateForm


class ListUsersView(ListView):
    model = AppUser
    context_object_name = 'users'
    template_name = 'users/list.html'


class CreateUserView(
    ModelFormMessagesMixin,
    NotLoginRequiredMixin,
    CreateView,
):
    form_class = UserCreateForm
    template_name = 'users/form.html'
    success_url = reverse_lazy('login')
    extra_context = {
        'title': _('Registration'),
    }
    valid_message = 'User is registered.'
    invalid_message = 'User registration error.'


class UpdateUserView(
    HandleNoPermissionMixin,
    ModelFormMessagesMixin,
    UserPassesTestOwnerMixin,
    UpdateView
):
    model = AppUser
    form_class = UserUpdateForm
    template_name = 'users/form.html'
    success_url = reverse_lazy('users:list')
    extra_context = {
        'title': _('Edit user'),
    }
    raise_exception = False
    valid_message = 'User data updated.'
    invalid_message = 'User update error.'


class DeleteUserView(
    HandleNoPermissionMixin,
    UserPassesTestOwnerMixin,
    ModelFormDeleteMessagesMixin,
    DeleteView
):
    model = AppUser
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users:list')
    valid_message = 'User deleted.'
    invalid_message = 'User deletion error.'
