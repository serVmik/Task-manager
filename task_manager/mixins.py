import logging

from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger('main_log')


class NotLoginRequiredMixin:
    """Verify that the current user is NOT authenticated."""

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class HandleNoPermissionMixin:
    """
    Set redirect url and messages,
    if the user is not authenticated or does not have permission.
    """
    message_no_permission = 'You are not authorized'
    logger_no_permission = message_no_permission
    url_no_permission = reverse_lazy('login')

    def handle_no_permission(self):
        logger.debug(_(self.logger_no_permission))
        messages.error(self.request, _(self.message_no_permission))
        return redirect(self.url_no_permission)


class CheckUserForOwnershipAccountMixin(UserPassesTestMixin):
    """Check if the user has owner permission on account."""

    def check_user_for_ownership(self):
        return self.get_object() == self.request.user

    def get_test_func(self):
        return self.check_user_for_ownership


class AuthorshipTaskCheckMixin(UserPassesTestMixin):
    """Check current user for authorship of task."""

    def authorship_check(self):
        author_pk = self.get_object().author.pk
        current_user_pk = self.request.user.pk
        return author_pk == current_user_pk

    def get_test_func(self):
        return self.authorship_check


class AddMessagesToFormSubmissionMixin:
    """Add a log and a flash messages on form submission."""

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
