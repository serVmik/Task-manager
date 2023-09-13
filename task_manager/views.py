from django.views.generic.base import TemplateView
from django.utils.translation import gettext_lazy as _


class HomeView(TemplateView):
    template_name = 'home.html'
    extra_context = {
        'title': _('Task manager'),
        'text': _('Task manager'),
        'greetings': 'Hello!',
    }
