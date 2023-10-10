import logging

from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.base import TemplateView
from django.utils.translation import gettext_lazy as _

from task_manager.mixins import AddMessagesToFormSubmissionMixin

logger = logging.getLogger('main_log')


class HomeView(TemplateView):
    template_name = 'home.html'


class UserLoginView(
    AddMessagesToFormSubmissionMixin,
    LoginView
):
    success_message = _('You are logged in')
    template_name = 'login.html'


class UserLogoutView(LogoutView):
    def get_default_redirect_url(self):
        logger.debug(_('You are logged out'))
        messages.info(self.request, _('You are logged out'))
        return super().get_default_redirect_url()
