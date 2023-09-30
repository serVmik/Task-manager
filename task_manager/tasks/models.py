from django.db import models
from django.urls import reverse_lazy

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.users.models import UserModel
from django.utils.translation import gettext_lazy as _


class Task(models.Model):
    name = models.CharField(
        max_length=127,
        unique=True,
        blank=False,
        error_messages={
            'unique': _('Such a task already exists!'),
        },
        help_text=_('<i>Input task name</i>'),
        # db_column='task_name',
    )
    description = models.TextField(blank=True)
    status = models.ForeignKey(Status, on_delete=models.PROTECT)

    labels = models.ManyToManyField(
        Label, related_name='labels',
        blank=True,
    )

    author = models.ForeignKey(
        UserModel, related_name='author',
        on_delete=models.PROTECT,
        blank=False,
    )
    executor = models.ForeignKey(
        UserModel, related_name='executor',
        on_delete=models.PROTECT,
        blank=True, null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('tasks', kwargs={'pk': self.pk})
