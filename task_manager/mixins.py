import logging

from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger('main_log')


class HandleNoPermissionMixin:
    """
    Add a redirect url and a messages,
    if the user doesn't have permission.
    """
    message_no_permission = 'You are not authorized'
    logger_no_permission = message_no_permission
    url_no_permission = reverse_lazy('login')

    def handle_no_permission(self):
        logger.debug(_(self.logger_no_permission))
        messages.error(self.request, _(self.message_no_permission))
        return redirect(self.url_no_permission)


class CheckUserForOwnershipAccountMixin(UserPassesTestMixin):
    """
    Check if the user has owner permission on account.
    """
    def authorship_check(self):
        current_user = self.get_object()
        specified_user = self.request.user
        self.logger_no_permission = self.message_no_permission

        if not self.request.user.is_authenticated:
            self.message_no_permission = 'You are not authorized'
            self.url_no_permission = reverse_lazy('login')
            return False
        elif current_user == specified_user:
            return True
        elif current_user != specified_user:
            self.url_no_permission = reverse_lazy('users:list')
            return False

    def get_test_func(self):
        return self.authorship_check


class CheckAuthorshipTaskMixin(UserPassesTestMixin):
    """
    Check current user for authorship of task.
    """
    def authorship_check(self):
        current_user = self.get_object().author.pk
        specified_user = self.request.user.pk
        self.logger_no_permission = self.message_no_permission

        if not self.request.user.is_authenticated:
            self.message_no_permission = 'You are not authorized'
            self.url_no_permission = reverse_lazy('login')
            return False
        elif current_user == specified_user:
            return True
        elif current_user != specified_user:
            self.url_no_permission = reverse_lazy('tasks:list')
            return False

    def get_test_func(self):
        return self.authorship_check


class AddMessagesToFormSubmissionMixin:
    """
    Add a log and a flash messages on form submission.
    """
    success_message = ''
    error_message = ''

    def form_valid(self, form):
        response = super().form_valid(form)
        logger.debug(self.success_message)
        messages.success(self.request, self.success_message)
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        logger.error(self.error_message)
        messages.error(self.request, self.error_message)
        return response


class RedirectForModelObjectDeleteErrorMixin:
    """
    Add protected_redirect_url when raise ProtectedError.
    Add protected_message when raise ProtectedError.
    """
    protected_redirect_url = 'home'
    protected_message = 'Cannot delete object because it is in use'

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            logger.error(self.protected_message)
            messages.error(request, self.protected_message)
            return redirect(self.protected_redirect_url)
