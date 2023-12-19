from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class TestFilterTask(TestCase):
    fixtures = ['users.json', 'statuses.json', 'labels.json', 'tasks.json']

    def setUp(self):
        """Create a test database"""
        self.user = User.objects.get(username='author')

    def test_filter_task_by_status(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse('tasks:list'),
            {'status': '1'},
        )
        html = response.content.decode()

        self.assertEquals(response.status_code, 200)
        self.assertInHTML('old', html)
