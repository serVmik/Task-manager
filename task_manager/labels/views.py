from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from .models import Label
from .forms import LabelForm


class ListLabelsView(ListView):
    model = Label
    template_name = 'labels/list.html'
    context_object_name = 'labels'


class CreateLabelView(CreateView):
    form_class = LabelForm
    template_name = 'labels/form.html'
    success_url = reverse_lazy('labels:list')
    extra_context = {'title': _('Create')}


class UpdateLabelView(UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/form.html'
    success_url = reverse_lazy('labels:list')
    extra_context = {'title': _('Update')}


class DeleteLabelView(DeleteView):
    model = Label
    template_name = 'labels/delete.html'
    success_url = reverse_lazy('labels:list')
