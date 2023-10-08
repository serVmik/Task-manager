import django_filters
from django.forms import CheckboxInput

from django.utils.translation import gettext_lazy as _

from task_manager.labels.models import Label
from task_manager.tasks.models import Task


class TaskFilter(django_filters.FilterSet):
    filtered_labels = django_filters.ModelChoiceFilter(
        queryset=Label.objects.all(),
        field_name='labels',
        label=_('Label'),
    )

    user_tasks_only = django_filters.BooleanFilter(
        field_name='author',
        label=_('Only your tasks'),
        method='get_tasks_current_user',
        widget=CheckboxInput,
    )

    def get_tasks_current_user(self, queryset, name, value):
        current_user = self.request.user.pk
        if value:
            tasks_current_user = queryset.filter(author=current_user)
            return tasks_current_user
        return queryset

    class Meta:
        model = Task
        fields = ['status', 'executor']
