from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from task_manager.mixins import test_flash_message

from task_manager.users.models import UserModel
from task_manager.users.views import (
    CreateUserView,
    ListUsersView,
    UpdateUserView,
    DeleteUserView,
)


class UserCrudTestCase(TestCase):

    def setUp(self):
        UserModel.objects.create(
            username='ivan_ivanov',
            first_name='Ivan',
            last_name='Ivanov',
        )

    def test_create_user(self):
        url_create = reverse('users:create')
        user_being_created = {
            'username': 'petr_petrov',
            'first_name': 'Petr',
            'last_name': 'Petrov',
            'password1': 'q1s2d3r4',
            'password2': 'q1s2d3r4',
        }

        # test whether the current_user is authenticated
        current_user = UserModel.objects.get(username='ivan_ivanov')
        self.client.force_login(current_user)
        response = self.client.get(url_create)
        self.assertEquals(response.status_code, 403)
        test_flash_message(response, _('Invalid action.'))
        self.client.logout()

        # page test, method=get
        response = self.client.get(url_create)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(url_create, '/users/create/')
        self.assertTemplateUsed(response, 'users/form.html')
        self.assertIs(response.resolver_match.func.view_class, CreateUserView)

        # page test, method=post
        response = self.client.post(url_create, user_being_created)
        self.assertEquals(url_create, '/users/create/')
        self.assertRedirects(response, reverse('login'), 302)
        self.assertIs(response.resolver_match.func.view_class, CreateUserView)
        test_flash_message(response, _('User is registered.'))

        # user create test
        user = UserModel.objects.get(username='petr_petrov')
        self.assertEquals(user.get_full_name(), 'Petr Petrov')
        self.assertTrue(user.check_password('q1s2d3r4'))

    def test_read_users(self):
        url_list = reverse('users:list')
        user = UserModel.objects.get(username='ivan_ivanov')

        # page test, method=get
        response = self.client.get(url_list)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(url_list, '/users/')
        self.assertTemplateUsed(response, 'users/list.html')
        self.assertIs(response.resolver_match.func.view_class, ListUsersView)

        # user read test
        html = response.content.decode()
        self.assertInHTML(str(user.pk), html)
        self.assertInHTML('ivan_ivanov', html)
        self.assertInHTML('Ivan Ivanov', html)
        self.assertInHTML(user.date_joined.strftime("%d-%m-%Y %H:%M"), html)

    def test_update_user(self):
        old_user_data = UserModel.objects.get(username='ivan_ivanov')
        url_update = reverse('users:update', kwargs={'pk': old_user_data.pk})
        new_user_data = {
            'username': 'ivanov_daryin',
            'first_name': 'Ivan',
            'last_name': 'Ivanov-Daryin',
            'password1': 'r4d3s2q1',
            'password2': 'r4d3s2q1',
        }
        self.client.force_login(old_user_data)

        # page test, method=get
        response = self.client.get(url_update)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(url_update, f'/users/{old_user_data.pk}/update/')
        self.assertTemplateUsed(response, 'users/form.html')
        self.assertIs(response.resolver_match.func.view_class, UpdateUserView)

        # page test, method=post
        response = self.client.post(url_update, new_user_data)
        self.assertEquals(url_update, f'/users/{old_user_data.pk}/update/')
        self.assertRedirects(response, reverse('users:list'), 302)
        self.assertIs(response.resolver_match.func.view_class, UpdateUserView)
        test_flash_message(response, _('User data updated.'))

        # user update test
        [current_user_data] = UserModel.objects.filter(pk=old_user_data.pk).values()  # noqa: E501
        for key in ('username', 'first_name', 'last_name'):
            self.assertEquals(new_user_data[key], current_user_data[key])
        current_user_data = UserModel.objects.get(pk=old_user_data.pk)
        self.assertTrue(current_user_data.check_password('r4d3s2q1'))

    def test_delete_user(self):
        user = UserModel.objects.get(username='ivan_ivanov')
        url_delete = reverse('users:delete', kwargs={'pk': user.pk})
        self.client.force_login(user)

        # page test, method=get
        response = self.client.get(url_delete)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(url_delete, f'/users/{user.pk}/delete/')
        self.assertTemplateUsed(response, 'users/delete.html')
        self.assertIs(response.resolver_match.func.view_class, DeleteUserView)

        # page test, method=post
        response = self.client.post(url_delete)
        self.assertEquals(url_delete, f'/users/{user.pk}/delete/')
        self.assertRedirects(response, reverse('users:list'), 302)
        self.assertIs(response.resolver_match.func.view_class, DeleteUserView)
        test_flash_message(response, _('User deleted.'))

        # user deletion test
        self.assertFalse(UserModel.objects.filter(username='ivan_ivanov').exists())  # noqa: E501
