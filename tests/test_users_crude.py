from django.test import TestCase

from django.urls import reverse

from task_manager.users.models import AppUser
from task_manager.users.views import UserListView


class UserCrudTestCase(TestCase):

    def setUp(self):
        AppUser.objects.create(
            username='ivan_ivanov',
            first_name='Ivan',
            last_name='Ivanov',
            password='q1s2d3r4',
        )

    def test_model(self):
        user_ivan = AppUser.objects.get(username='ivan_ivanov')
        self.assertEquals(user_ivan.first_name, 'Ivan')
        self.assertEquals(user_ivan.last_name, 'Ivanov')
        self.assertEquals(user_ivan.get_full_name(), 'Ivan Ivanov')

    def test_create(self):
        url_create = reverse('users:create')
        url_list_users = reverse('users:list')
        user_petr = {
            'username': 'petr_petrov',
            'first_name': 'Petr',
            'last_name': 'Petrov',
            'password1': 'q1s2d3r4',
            'password2': 'q1s2d3r4',
        }

        self.client.post(url_create, user_petr)
        response = self.client.get(url_list_users)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(url_list_users, '/users/')
        self.assertTemplateUsed(response, 'users/list.html')
        self.assertIs(response.resolver_match.func.view_class, UserListView)

        self.assertInHTML('ivan_ivanov', response.content.decode())
        self.assertInHTML('Ivan Ivanov', response.content.decode())
        self.assertInHTML('petr_petrov', response.content.decode())
        self.assertInHTML('Petr Petrov', response.content.decode())

    # def test_html_update(self):
    #     pass

    # def test_html_delete(self):
    #     pass
