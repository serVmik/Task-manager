from django.db import models
from django.urls import reverse_lazy

from task_manager.labels.models import LabelModel
from task_manager.statuses.models import Status
from task_manager.users.models import AppUser


class TaskModel(models.Model):
    name = models.CharField(max_length=127, unique=True, blank=False)
    description = models.TextField(blank=True)
    status = models.ForeignKey(Status, on_delete=models.PROTECT)

    labels = models.ManyToManyField(
        LabelModel,
        blank=True,
        related_name='labels',
    )

    author = models.ForeignKey(
        AppUser,
        on_delete=models.PROTECT,
        blank=False,
        related_name='author',
    )
    executor = models.ForeignKey(
        AppUser,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name='executor',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('tasks', kwargs={'pk': self.pk})
