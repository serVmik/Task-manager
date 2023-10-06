import logging

from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger('main_log')


class NotLoginRequiredMixin:
    """
    Verify that the current user is NOT authenticated.
    """
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


class ProtectUserFromDeletionIfUserUsingMixin:
    """
    Add a refusal to delete a model object
    if this object is used in another model.
    Add a protected_message about protecting an object from deletion.
    Add a protected_redirect_url in case of refusal.
    """
    protected_message = 'Cannot delete object because it is in use'
    protected_redirect_url = 'home'

    def check_object_for_use(self, request):
        """
        Check model object for use in another models.
        Add a protected_message about protecting an object from deletion.
        """
        is_use = False

        if self.get_object().author.count():
            is_use = True
        elif self.get_object().executor.count():
            is_use = True

        if is_use:
            messages.error(request, self.protected_message)

        return is_use

    def post(self, request, *args, **kwargs):
        """
        Add a protected_redirect_url in case of refusal.
        """
        if self.check_object_for_use(request):
            return redirect(self.protected_redirect_url)
        return super().post(request, *args, **kwargs)
