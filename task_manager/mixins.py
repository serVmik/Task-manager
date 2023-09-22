from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin, UserPassesTestMixin
from django.contrib.messages import get_messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

import logging

logger = logging.getLogger('main_log')


class UserPassesTestOwnerMixin(UserPassesTestMixin):
    """
    Test whether the user has owner permission.
    """

    def test_func(self):
        return self.get_object() == self.request.user

    def handle_no_permission(self):
        messages.error(
            self.request,
            _('Only the owner can edit and delete user.')
        )
        return redirect(reverse_lazy('users:list'))


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


def test_flash_message(response, expected_message):
    """
    Test whether message in response.
    Test whether message corresponds to the expected message.
    """

    number_of_messages = 1
    current_message = get_messages(response.wsgi_request)
    assert len(current_message) == number_of_messages
    assert str(*current_message) == expected_message
