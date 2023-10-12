from django.contrib.auth.models import AbstractUser
from django.urls import reverse_lazy


class UserModel(AbstractUser):

    def __str__(self):
        return self.get_full_name()

    def get_absolute_url(self):
        return reverse_lazy('users:show', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['username']
