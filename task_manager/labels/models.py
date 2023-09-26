from django.db import models
from django.urls import reverse_lazy


class LabelModel(models.Model):
    name = models.CharField(
        max_length=127,
        unique=True,
        blank=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('labels', kwargs={'pk': self.pk})
