from django.contrib.auth import get_user_model
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from .forms import UserCreateForm, UserUpdateForm
from ..mixins import (
    AddMessagesToFormSubmissionMixin,
    CheckUserForOwnershipAccountMixin,
    HandleNoPermissionMixin,
    RedirectForModelObjectDeleteErrorMixin,
)

User = get_user_model()


class ListUsersView(ListView):
    model = User
    context_object_name = 'users'
    template_name = 'users/list.html'


class CreateUserView(
    HandleNoPermissionMixin,
    AddMessagesToFormSubmissionMixin,
    CreateView,
):
    form_class = UserCreateForm
    template_name = 'form.html'
    success_url = reverse_lazy('login')
    url_no_permission = reverse_lazy('users:list')
    extra_context = {
        'title': _('Registration'),
        'btn_name': _('Register'),
    }

    success_message = _('User successfully registered')
    error_message = _('User registration error')
    message_no_permission = _('You are already logged in')


class UpdateUserView(
    HandleNoPermissionMixin,
    CheckUserForOwnershipAccountMixin,
    AddMessagesToFormSubmissionMixin,
    UpdateView,
):
    model = User
    form_class = UserUpdateForm
    template_name = 'form.html'
    success_url = reverse_lazy('users:list')
    url_no_permission = reverse_lazy('users:list')
    extra_context = {
        'title': _('Edit user'),
        'btn_name': _('Edit'),
    }

    success_message = _('User successfully updated')
    error_message = _('User update error')
    message_no_permission = _('Only the owner can update users data')


class DeleteUserView(
    HandleNoPermissionMixin,
    CheckUserForOwnershipAccountMixin,
    RedirectForModelObjectDeleteErrorMixin,
    AddMessagesToFormSubmissionMixin,
    DeleteView,
):
    model = User
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users:list')
    protected_redirect_url = reverse_lazy('users:list')
    extra_context = {
        'title': _('Deleting a user'),
    }

    success_message = _('User deleted successfully')
    error_message = _('User deletion error')
    message_no_permission = _('Only the owner can delete account')
    protected_message = _('Cannot delete user because it is in use')
