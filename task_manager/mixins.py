from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


class TestUserAuthorizationMixin(UserPassesTestMixin):

    def test_func(self):
        return self.request.user.pk == self.get_object().pk


class AppUserPassesTestMixin(UserPassesTestMixin):
    def test_func(self):
        return self.get_object() == self.request.user

    def handle_no_permission(self):
        messages.error(self.request,
                       _('Only the owner can edit and delete user.'))
        return redirect(reverse_lazy('users:list'))
