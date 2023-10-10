from django.db import models
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


class Label(models.Model):
    name = models.CharField(
        max_length=127,
        unique=True,
        blank=False,
        verbose_name=_('Name'),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('labels', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Метка'
        verbose_name_plural = 'Метки'
