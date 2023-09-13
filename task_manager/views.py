from django.views.generic.base import TemplateView


class HomeView(TemplateView):
    template_name = 'home.html'
    extra_context = {
        'title': 'Task manager',
        'text': 'Task manager',
        'greetings': 'Hello!',
    }
