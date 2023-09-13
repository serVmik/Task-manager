from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.translation import gettext_lazy as _

from .models import AppUser
from .forms import UserCreateForm, UserUpdateForm


class UserListView(ListView):
    model = AppUser
    template_name = 'users/list.html'
    context_object_name = 'users'


class UserCreateView(CreateView):
    model = AppUser
    template_name = 'users/create.html'
    form_class = UserCreateForm
    extra_context = {
        'title': _('Registration')
    }


class UserUpdateView(UpdateView):
    model = AppUser
    template_name = 'users/update.html'
    form_class = UserUpdateForm


class UserDeleteView(DeleteView):
    model = AppUser
    template_name = 'users/delete.html'
