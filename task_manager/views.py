from django.views.generic.base import TemplateView


class IndexView(TemplateView):
    template_name = 'index.html'
    extra_context = {
        'title': 'Task manager',
        'text': 'Task manager',
        'greetings': 'Hello!',
    }
