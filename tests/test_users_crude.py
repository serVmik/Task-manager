from django.test import TestCase

from django.urls import reverse

from task_manager.users.models import AppUser

username = 'ivan_ivanov'
first_name = 'Ivan'
last_name = 'Ivanov'
full_name = f'{first_name} {last_name}'


class UserCrudTestCase(TestCase):

    def setUp(self):
        AppUser.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
        )

    def test_model(self):
        user = AppUser.objects.get(username=username)
        self.assertEquals(user.username, username)
        self.assertEquals(user.first_name, first_name)
        self.assertEquals(user.last_name, last_name)

    # def test_create(self):
    #     pass

    def test_html_reade(self):
        url = reverse('users:list')
        response = self.client.get(url)

        self.assertEquals(url, '/users/')
        self.assertEquals(response.status_code, 200)
        self.assertInHTML(username, response.content.decode())
        self.assertInHTML(full_name, response.content.decode())

    # def test_html_update(self):
    #     pass

    # def test_html_delete(self):
    #     pass
