from django.views.generic import ListView

from .models import AppUser


class AppUserListView(ListView):
    model = AppUser
    template_name = 'users/list.html'
    context_object_name = 'users'
