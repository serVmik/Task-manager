import logging

from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.base import TemplateView
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger('main_log')


class HomeView(TemplateView):
    template_name = 'home.html'


class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = 'login.html'

    def form_valid(self, form):
        logger.debug('User is logged in')
        response = super().form_valid(form)
        messages.success(self.request, _('You are logged in'))
        return response

    def form_invalid(self, form):
        logger.error('Error authentication')
        response = super().form_invalid(form)
        messages.error(self.request, _('Error authentication'))
        return response


class UserLogoutView(LogoutView):
    def get_default_redirect_url(self):
        messages.info(self.request, _('You are logged out'))
        return super().get_default_redirect_url()
