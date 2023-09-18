from django.test import TestCase
from task_manager.users.models import AppUser


class AppUserTestCase(TestCase):
    def setUp(self):
        AppUser.objects.create(
            username='ivan_ivanov',
            first_name='Ivan',
            last_name='Ivanov',
        )

    def test_name(self):
        ivan_ivanov = AppUser.objects.get(username='ivan_ivanov')
        self.assertEquals(ivan_ivanov.first_name, 'Ivan')
        self.assertEquals(ivan_ivanov.last_name, 'Ivanov')
