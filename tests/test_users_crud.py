from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from tests.tests_func import flash_message_test
from task_manager.users.forms import UserCreateForm, UserUpdateForm
from task_manager.users.views import (CreateUserView, ListUsersView,
                                      UpdateUserView, DeleteUserView,)

User = get_user_model()

# add user permission test


class UserCrudTestCase(TestCase):

    def setUp(self):
        User.objects.create(
            username='ivan_ivanov',
            first_name='Ivan',
            last_name='Ivanov',
        )

    def test_create_user(self):
        user_being_created = {
            'username': 'petr_petrov',
            'first_name': 'Petr',
            'last_name': 'Petrov',
            'password1': 'q1s2d3r4',
            'password2': 'q1s2d3r4',
        }
        url = reverse('users:create')

        self.assertFalse(User.objects.filter(username='petr_petrov').exists())

        # test whether the current_user is authenticated
        current_user = User.objects.get(username='ivan_ivanov')
        self.client.force_login(current_user)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)
        flash_message_test(response, _('You are already logged in!'))
        self.client.logout()

        # page test, method=get
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(url, '/users/create/')
        self.assertTemplateUsed(response, 'users/form.html')
        self.assertIs(response.resolver_match.func.view_class, CreateUserView)
        self.assertIsInstance(response.context['form'], UserCreateForm)

        # page test, method=post
        response = self.client.post(url, user_being_created)
        self.assertEquals(url, '/users/create/')
        self.assertRedirects(response, reverse('login'), 302)
        self.assertIs(response.resolver_match.func.view_class, CreateUserView)
        flash_message_test(response, _('User is registered.'))

        # user create test
        user = User.objects.get(username='petr_petrov')
        self.assertEquals(user.get_full_name(), 'Petr Petrov')
        self.assertTrue(user.check_password('q1s2d3r4'))

# add negative user creation test

    def test_read_users(self):
        user = User.objects.get(username='ivan_ivanov')
        url = reverse('users:list')

        # page test, method=get
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(url, '/users/')
        self.assertTemplateUsed(response, 'users/list.html')
        self.assertIs(response.resolver_match.func.view_class, ListUsersView)

        # user read test
        html = response.content.decode()
        self.assertInHTML(str(user.pk), html)
        self.assertInHTML('ivan_ivanov', html)
        self.assertInHTML('Ivan Ivanov', html)
        self.assertInHTML(user.date_joined.strftime("%d-%m-%Y %H:%M"), html)

    def test_update_user(self):
        old_user_data = User.objects.get(username='ivan_ivanov')
        new_user_data = {
            'username': 'ivanov_daryin',
            'first_name': 'Ivan',
            'last_name': 'Ivanov-Daryin',
            'password1': 'r4d3s2q1',
            'password2': 'r4d3s2q1',
        }
        url = reverse('users:update', kwargs={'pk': old_user_data.pk})

        self.client.force_login(old_user_data)

        # page test, method=get
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(url, f'/users/{old_user_data.pk}/update/')
        self.assertTemplateUsed(response, 'users/form.html')
        self.assertIs(response.resolver_match.func.view_class, UpdateUserView)
        self.assertIsInstance(response.context['form'], UserUpdateForm)

        # page test, method=post
        response = self.client.post(url, new_user_data)
        self.assertEquals(url, f'/users/{old_user_data.pk}/update/')
        self.assertRedirects(response, reverse('users:list'), 302)
        self.assertIs(response.resolver_match.func.view_class, UpdateUserView)
        flash_message_test(response, _('User data updated.'))

        # user update test
        [current_user_data] = User.objects.filter(pk=old_user_data.pk).values()
        for key in ('username', 'first_name', 'last_name'):
            self.assertEquals(new_user_data[key], current_user_data[key])
        current_user_data: User = User.objects.get(pk=old_user_data.pk)
        self.assertTrue(current_user_data.check_password('r4d3s2q1'))

    def test_delete_user(self):
        user = User.objects.get(username='ivan_ivanov')
        url = reverse('users:delete', kwargs={'pk': user.pk})

        self.client.force_login(user)

        # page test, method=get
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(url, f'/users/{user.pk}/delete/')
        self.assertTemplateUsed(response, 'users/delete.html')
        self.assertIs(response.resolver_match.func.view_class, DeleteUserView)

        # page test, method=post
        response = self.client.post(url)
        self.assertEquals(url, f'/users/{user.pk}/delete/')
        self.assertRedirects(response, reverse('users:list'), 302)
        self.assertIs(response.resolver_match.func.view_class, DeleteUserView)
        flash_message_test(response, _('User deleted.'))

        # user deletion test
        self.assertFalse(User.objects.filter(username='ivan_ivanov').exists())
