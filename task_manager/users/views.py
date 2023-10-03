from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from .forms import UserCreateForm, UserUpdateForm
from .models import UserModel
from ..mixins import (
    NotLoginRequiredMixin,
    HandleNoPermissionMixin,
    OwnerUserPassesTestMixin,
    ModelFormMessagesMixin,
)


class ListUsersView(ListView):
    model = UserModel
    context_object_name = 'users'
    template_name = 'users/list.html'


class CreateUserView(
    HandleNoPermissionMixin,
    NotLoginRequiredMixin,
    ModelFormMessagesMixin,
    CreateView,
):
    form_class = UserCreateForm
    template_name = 'users/form.html'
    success_url = reverse_lazy('login')
    extra_context = {
        'title': _('Registration'),
    }
    success_message = 'User is registered.'
    error_message = 'User registration error.'
    message_no_permission = 'You are already logged in!'
    url_no_permission = reverse_lazy('users:list')


class UpdateUserView(
    HandleNoPermissionMixin,
    OwnerUserPassesTestMixin,
    ModelFormMessagesMixin,
    UpdateView,
):
    model = UserModel
    form_class = UserUpdateForm
    template_name = 'users/form.html'
    success_url = reverse_lazy('users:list')
    extra_context = {
        'title': _('Edit user'),
    }
    success_message = 'User data updated.'
    error_message = 'User update error.'


class DeleteUserView(
    HandleNoPermissionMixin,
    OwnerUserPassesTestMixin,
    ModelFormMessagesMixin,
    DeleteView,
):
    model = UserModel
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users:list')
    success_message = 'User deleted.'
    error_message = 'User deletion error.'
