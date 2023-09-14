from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy

import logging

logger = logging.getLogger('main_log')


class HomeView(TemplateView):
    logger.debug('Hello!')
    template_name = 'home.html'


class UserLoginView(LoginView):
    template_name = 'login.html'


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('login')
