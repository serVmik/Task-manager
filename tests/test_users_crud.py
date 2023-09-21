from django.test import TestCase

from django.urls import reverse

from task_manager.users.models import AppUser
from task_manager.users.views import (UserListView, UserUpdateView,
                                      UserDeleteView)


class UserCrudTestCase(TestCase):

    def setUp(self):
        AppUser.objects.create(
            username='ivan_ivanov',
            first_name='Ivan',
            last_name='Ivanov',
        )

    def test_model_user(self):
        user = AppUser.objects.get(username='ivan_ivanov')
        self.assertEquals(user.first_name, 'Ivan')
        self.assertEquals(user.last_name, 'Ivanov')
        self.assertEquals(user.get_full_name(), 'Ivan Ivanov')

    def test_create_user(self):
        url_create = reverse('users:create')
        url_list = reverse('users:list')
        created_user = {
            'username': 'petr_petrov',
            'first_name': 'Petr',
            'last_name': 'Petrov',
            'password1': 'q1s2d3r4',
            'password2': 'q1s2d3r4',
        }

        self.client.post(url_create, created_user)
        response = self.client.get(url_list)

        # test page
        self.assertEquals(response.status_code, 200)
        self.assertEquals(url_list, '/users/')
        self.assertTemplateUsed(response, 'users/list.html')
        self.assertIs(response.resolver_match.func.view_class, UserListView)

        # test page content
        html = response.content.decode()
        self.assertInHTML('ivan_ivanov', html)
        self.assertInHTML('Ivan Ivanov', html)
        self.assertInHTML('petr_petrov', html)
        self.assertInHTML('Petr Petrov', html)

    def test_update_user(self):
        user = AppUser.objects.get(username='ivan_ivanov')
        url_update = reverse('users:update', kwargs={'pk': user.pk})
        self.client.force_login(user)

        # test page
        response = self.client.get(url_update)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(url_update, f'/users/{user.pk}/update/')
        self.assertTemplateUsed(response, 'users/form.html')
        self.assertIs(response.resolver_match.func.view_class, UserUpdateView)

        # test update names
        new_user_data = {
            'username': 'ivanov_daryin',
            'first_name': 'Ivan',
            'last_name': 'Ivanov-Daryin',
            'password1': 'r4d3s2q1',
            'password2': 'r4d3s2q1',
        }
        self.client.post(url_update, new_user_data)
        current_user_data = AppUser.objects.filter(pk=user.pk)
        [current_user_data] = current_user_data.all().values()
        for key in ('username', 'first_name', 'last_name'):
            self.assertEquals(new_user_data[key], current_user_data[key])

        # test update password
        current_user_data = AppUser.objects.get(pk=user.pk)
        self.assertTrue(current_user_data.check_password('r4d3s2q1'))

    def test_delete_user(self):
        user = AppUser.objects.get(username='ivan_ivanov')
        self.client.force_login(user)
        url_delete = reverse('users:delete', kwargs={'pk': user.pk})

        # test page method=get
        response = self.client.get(url_delete)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(url_delete, f'/users/{user.pk}/delete/')
        self.assertTemplateUsed(response, 'users/delete.html')
        self.assertIs(response.resolver_match.func.view_class, UserDeleteView)

        # test page method=post
        response = self.client.post(url_delete)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(url_delete, f'/users/{user.pk}/delete/')
        self.assertRedirects(response, reverse('users:list'))
        self.assertIs(response.resolver_match.func.view_class, UserDeleteView)

        # test whether the user is deleted
        self.assertFalse(AppUser.objects.filter(username='ivan_ivanov').exists())  # noqa: E501
        # with self.assertRaises(ObjectDoesNotExist):
        #     AppUser.objects.get(username='ivan_ivanov')
