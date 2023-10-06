from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse_lazy

from task_manager.labels.models import Label
from tests.mixins import flash_message_test

User = get_user_model()


class TestReadLabelsList(TestCase):
    fixtures = ['users.json', 'statuses.json', 'labels.json', 'tasks.json']

    def test_read_labels_list(self):
        context_object = Label.objects.all()
        label = context_object.first()
        self.client.force_login(User.objects.first())
        response = self.client.get(reverse_lazy('labels:list'))
        html = response.content.decode()

        self.assertEquals(response.status_code, 200)
        self.assertInHTML(str(label.pk), html)
        self.assertInHTML(str(label.name), html)
        self.assertInHTML(label.created_at.strftime('%d-%m-%Y %H:%M'), html)
        # self.assertQuerysetEqual(
        #     response.context['labels'].order_by('id'),
        #     context_object.order_by('id')
        # )

    def test_read_labels_list_by_guest(self):
        response = self.client.get(reverse_lazy('labels:list'))
        self.assertRedirects(response, '/login/', 302)
        flash_message_test(response, 'You are not authorized')

    # add test paginate


class TestCreateLabel(TestCase):
    fixtures = ['users.json', 'statuses.json', 'labels.json', 'tasks.json']

    # def setUp(self):
    #     self.author =

