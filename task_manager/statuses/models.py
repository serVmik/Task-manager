from django.db import models
from django.urls import reverse


class Status(models.Model):
    name = models.CharField(max_length=63, unique=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('statuses', kwargs={'pk': self.pk})
