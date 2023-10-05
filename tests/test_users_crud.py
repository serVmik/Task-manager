from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _

from tests.mixins import flash_message_test
from task_manager.users.forms import UserCreateForm, UserUpdateForm


User = get_user_model()


class TestReadUsersList(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        self.user = User.objects.get(username='author')
        self.url = reverse_lazy('users:list')

    def test_read_users_list_by_anonymous(self):
        response = self.client.get(self.url)
        html = response.content.decode()

        self.assertEquals(response.status_code, 200)
        self.assertEquals(self.url, '/users/')
        self.assertInHTML(str(self.user.id), html)
        self.assertInHTML(str(self.user.username), html)
        self.assertInHTML(str(self.user), html)
        self.assertInHTML(self.user.date_joined.strftime("%d-%m-%Y %H:%M"), html)


class TestCreateUser(TestCase):
    fixtures = ['users.json', 'statuses.json', 'labels.json', 'tasks.json']

    def setUp(self):
        self.user_being_created = {
            'username': 'petr_petrov',
            'first_name': 'Petr',
            'last_name': 'Petrov',
            'password1': 'q1s2d3r4',
            'password2': 'q1s2d3r4',
        }
        self.url = reverse('users:create')

    def test_create_user_method_get(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(self.url, '/users/create/')
        self.assertTemplateUsed(response, 'users/form.html')
        self.assertIsInstance(response.context['form'], UserCreateForm)

    def test_create_user_method_post(self):
        response = self.client.post(self.url, self.user_being_created)
        self.assertRedirects(response, reverse('login'), 302)
        flash_message_test(response, _('User is registered'))

    def test_create_user(self):
        self.assertFalse(User.objects.filter(username='petr_petrov').exists())
        self.client.post(self.url, self.user_being_created)
        user = User.objects.get(username='petr_petrov')

        self.assertEquals(user.get_full_name(), 'Petr Petrov')
        self.assertTrue(user.check_password('q1s2d3r4'))

    def test_create_user_by_authorized_user(self):
        current_user = User.objects.get(username='author')
        self.client.force_login(current_user)

        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('users:list'), 302)
        flash_message_test(response, _('You are already logged in!'))

    def test_create_user_error(self):
        user_being_created = {'username': 'petr_error'}
        response = self.client.post(self.url, user_being_created)

        self.assertEquals(response.status_code, 200)
        flash_message_test(response, _('User registration error'))


class TestUpdateUser(TestCase):
    fixtures = ['users.json', 'statuses.json', 'labels.json', 'tasks.json']

    def setUp(self):
        self.old_user_data = User.objects.get(username='executor')
        self.new_user_data = {
            'username': 'happy_married_executor',
            'first_name': 'Olga',
            'last_name': 'Popova',
            'password1': 'r4d3s2q1',
            'password2': 'r4d3s2q1',
        }
        self.url = reverse(
            'users:update',
            kwargs={
                'pk': self.old_user_data.pk
            }
        )

    def test_update_user_method_get(self):
        self.client.force_login(self.old_user_data)
        response = self.client.get(self.url)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(self.url, f'/users/{self.old_user_data.pk}/update/')
        self.assertTemplateUsed(response, 'users/form.html')
        self.assertIsInstance(response.context['form'], UserUpdateForm)

    def test_update_user_method_post(self):
        self.client.force_login(self.old_user_data)
        response = self.client.post(self.url, self.new_user_data)

        self.assertEquals(self.url, f'/users/{self.old_user_data.pk}/update/')
        self.assertRedirects(response, reverse('users:list'), 302)
        flash_message_test(response, _('User data updated'))

    def test_update_user(self):
        self.client.force_login(self.old_user_data)
        self.client.post(self.url, self.new_user_data)

        [current_user_data] = User.objects.filter(
            pk=self.old_user_data.pk
        ).values()

        for key in ('username', 'first_name', 'last_name'):
            self.assertEquals(self.new_user_data[key], current_user_data[key])

        current_user_data: User = User.objects.get(pk=self.old_user_data.pk)
        self.assertTrue(current_user_data.check_password('r4d3s2q1'))

    def test_update_user_by_another_user(self):
        owner_user = User.objects.get(username='author')
        another_user = User.objects.get(username='not_author')
        url = reverse('users:update', kwargs={'pk': owner_user.pk})

        self.client.force_login(another_user)
        response = self.client.get(url, self.new_user_data)

        self.assertRedirects(response, reverse('users:list'), 302)
        flash_message_test(response, 'Only the owner can update users data')


class TestDeleteUser(TestCase):
    fixtures = ['users.json', 'statuses.json', 'labels.json', 'tasks.json']

    def setUp(self):
        self.user = User.objects.get(username='author')
        self.not_author = User.objects.get(username='not_author')
        self.url = reverse('users:delete', kwargs={'pk': self.user.pk})

    def test_delete_user_by_anonymous(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('login'), 302)
        flash_message_test(response, _('You are not authorized'))
        self.assertTrue(User.objects.filter(username='author').exists())

    # def test_delete_user_by_not_owner(self):
    #     self.client.force_login(self.not_author)
    #     response = self.client.get(self.url)
    #     self.assertRedirects(response, reverse('users:list'), 302)
    #     flash_message_test(response, _('Only the owner can delete account'))

#
#         self.client.force_login(user)
#
#         # page test, method=get
#         response = self.client.get(url)
#         self.assertEquals(response.status_code, 200)
#         self.assertEquals(url, f'/users/{user.pk}/delete/')
#         self.assertTemplateUsed(response, 'users/delete.html')
#         self.assertIs(response.resolver_match.func.view_class, DeleteUserView)
#
#         # page test, method=post
#         response = self.client.post(url)
#         self.assertEquals(url, f'/users/{user.pk}/delete/')
#         self.assertRedirects(response, reverse('users:list'), 302)
#         self.assertIs(response.resolver_match.func.view_class, DeleteUserView)
#         flash_message_test(response, _('User deleted.'))
#
#         # user deletion test
#         self.assertFalse(User.objects.filter(username='ivan_ivanov').exists())
