from django.contrib import messages
from django.contrib.auth.mixins import (
    AccessMixin,
    UserPassesTestMixin,
)
from django.contrib.messages import get_messages
from django.shortcuts import redirect
from django.views.generic import DeleteView
from django.views.generic.edit import ModelFormMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

import logging

logger = logging.getLogger('main_log')


class NotLoginRequiredMixin(AccessMixin):
    """
    Verify that the current user is NOT authenticated.
    """

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logger.debug('Invalid action.')
            messages.error(self.request, _('Invalid action.'))
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class HandleNoPermissionMixin(AccessMixin):
    """
    Redirects the authenticated user.

    Overrides method django.contrib.auth.mixins.AccessMixin.
    """

    def handle_no_permission(self):
        logger.error('Invalid action.')
        messages.error(self.request, _('Invalid action.'))
        return redirect(reverse_lazy('login'))


class ModelFormMessagesMixin(ModelFormMixin):
    """
    Sets the text for log messages.
    Sets the text for flash messages.

    Use it only in CreateView, UpdateView.
    Overrides methods django.views.generic.edit.ModelFormMixin.
    """

    valid_message = ''
    invalid_message = ''

    def form_valid(self, form):
        response = super().form_valid(form)
        logger.debug(self.valid_message)
        messages.success(self.request, self.valid_message)
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        logger.error(self.invalid_message)
        messages.error(self.request, self.invalid_message)
        return response


class ModelFormDeleteMessagesMixin(DeleteView):
    """
    Sets the text for log messages.
    Sets the text for flash messages.

    Use it only in DeleteView.
    Overrides methods django.views.generic.DeleteView.
    """

    valid_message = ''
    invalid_message = ''

    def form_valid(self, form):
        response = super().form_valid(form)
        logger.debug(self.valid_message)
        messages.success(self.request, self.valid_message)
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        logger.error(self.invalid_message)
        messages.error(self.request, self.invalid_message)
        return response


class UserPassesTestOwnerMixin(UserPassesTestMixin):
    """
    Test whether the user has owner permission.

    Overrides methods django.contrib.auth.mixins.UserPassesTestMixin.
    """

    def test_func(self):
        return self.get_object() == self.request.user

    def handle_no_permission(self):
        messages.error(
            self.request,
            _('Only the owner can edit and delete user.')
        )
        return redirect(reverse_lazy('users:list'))


def test_flash_message(response, expected_message):
    """
    Test whether message in response.
    Test whether message corresponds to the expected message.
    """

    number_of_messages = 1
    current_message = get_messages(response.wsgi_request)
    assert len(current_message) == number_of_messages
    assert str(*current_message) == expected_message
