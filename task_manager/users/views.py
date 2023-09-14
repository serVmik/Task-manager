from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from ..mixins import TestUserAuthorizationMixin
from .models import AppUser
from .forms import UserCreateForm, UserUpdateForm


class UserListView(ListView):
    model = AppUser
    context_object_name = 'users'
    template_name = 'users/list.html'


class UserCreateView(CreateView):
    form_class = UserCreateForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('login')


class UserUpdateView(LoginRequiredMixin, TestUserAuthorizationMixin, UpdateView):
    model = AppUser
    form_class = UserUpdateForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('login')


class UserDeleteView(LoginRequiredMixin, TestUserAuthorizationMixin, DeleteView):
    model = AppUser
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users:list')
