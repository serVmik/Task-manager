from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.views.generic.base import TemplateView
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _


class HomeView(TemplateView):
    template_name = 'home.html'
    extra_context = {
        'title': _('Task manager'),
        'text': _('Task manager'),
        'greetings': _('Hello!'),
    }


class UserLoginView(LoginView):
    form_class = AuthenticationForm
    template_name = 'login.html'
    extra_context = {
        'title': _('Login'),
    }


def logout_user(request):
    logout(request)
    return redirect('login')
