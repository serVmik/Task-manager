from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from .forms import UserCreateForm, UserUpdateForm
from .models import UserModel
from ..mixins import (
    NotLoginRequiredMixin,
    HandleNoPermissionMixin,
    CheckUserForOwnershipAccountMixin,
    AddMessagesToFormSubmissionMixin,
    RedirectForModelObjectDeleteErrorMixin,
)


class ListUsersView(ListView):
    model = UserModel
    context_object_name = 'users'
    template_name = 'users/list.html'


class CreateUserView(
    HandleNoPermissionMixin,
    NotLoginRequiredMixin,
    AddMessagesToFormSubmissionMixin,
    CreateView,
):
    form_class = UserCreateForm
    template_name = 'users/form.html'
    success_url = reverse_lazy('login')
    extra_context = {
        'title': _('Registration'),
    }
    success_message = _('User is registered')
    error_message = _('User registration error')
    message_no_permission = _('You are already logged in!')
    url_no_permission = reverse_lazy('users:list')


class UpdateUserView(
    HandleNoPermissionMixin,
    CheckUserForOwnershipAccountMixin,
    AddMessagesToFormSubmissionMixin,
    UpdateView,
):
    model = UserModel
    form_class = UserUpdateForm
    template_name = 'users/form.html'
    success_url = reverse_lazy('users:list')
    extra_context = {
        'title': _('Edit user'),
    }
    success_message = _('User data updated')
    error_message = _('User update error')
    message_no_permission = _('Only the owner can update users data')
    url_no_permission = reverse_lazy('users:list')


class DeleteUserView(
    HandleNoPermissionMixin,
    CheckUserForOwnershipAccountMixin,
    RedirectForModelObjectDeleteErrorMixin,
    AddMessagesToFormSubmissionMixin,
    DeleteView,
):
    model = UserModel
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users:list')
    success_message = _('User deleted')
    error_message = _('User deletion error')
    message_no_permission = _('Only the owner can delete account')
    protected_message = _('Cannot delete user because it is in use')
    protected_redirect_url = reverse_lazy('users:list')
