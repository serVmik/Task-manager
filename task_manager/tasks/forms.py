from django.forms import ModelForm

from task_manager.tasks.models import TaskModel


class TaskForm(ModelForm):

    class Meta:
        model = TaskModel
        fields = ('name', 'description', 'status',
                  'executor', 'labels')
