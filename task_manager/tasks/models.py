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
            'unique': _('Such a task already exists'),
        },
        help_text='<i>' + _('Required field') + '</i>',
        verbose_name=_('Name')
    )
    description = models.TextField(
        blank=True,
        verbose_name=_('Description')
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        help_text='<i>' + _('Required field') + '</i>',
        verbose_name=_('Status'),
    )
    labels = models.ManyToManyField(
        Label, related_name='labels',
        through='TaskLabelRelation',
        blank=True,
        verbose_name=_('Labels')
    )
    author = models.ForeignKey(
        UserModel, related_name='author',
        on_delete=models.PROTECT,
        blank=False,
        verbose_name=_('Author'),
    )
    executor = models.ForeignKey(
        UserModel, related_name='executor',
        on_delete=models.PROTECT,
        blank=True, null=True,
        verbose_name=_('Executor'),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Date of creation'),
    )
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('tasks', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
        ordering = ['created_at', 'name']


class TaskLabelRelation(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    label = models.ForeignKey(Label, on_delete=models.PROTECT)
