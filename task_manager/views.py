from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

import logging

logger = logging.getLogger('main_log')


class HomeView(TemplateView):
    template_name = 'home.html'


class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = 'login.html'

    success_message = _('Welcome, you are logged in!')
    if success_message:
        logger.debug('User is logged in, id_username = ')
    else:
        logger.warning('Error authentication')


class UserLogoutView(SuccessMessageMixin, LogoutView):
    next_page = reverse_lazy('login')
    success_message = _('You are logged out!')
