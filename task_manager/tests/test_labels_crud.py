from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from task_manager.labels.forms import LabelForm
from task_manager.labels.models import Label
from task_manager.tests.testing_functions import flash_message_test

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

    def test_read_labels_list_by_guest(self):
        response = self.client.get(reverse_lazy('labels:list'))
        self.assertRedirects(response, reverse_lazy('login'), 302)
        flash_message_test(response, _('You are not authorized'))

    # add test paginate


class TestCreateLabel(TestCase):
    fixtures = ['users.json', 'statuses.json', 'labels.json', 'tasks.json']

    def setUp(self):
        self.author = User.objects.get(username='author')
        self.data_for_label = {
            "name": "created_label",
        }
        self.url = reverse_lazy('labels:create')

    def test_create_label_successfully(self):
        self.client.force_login(self.author)

        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        self.assertIsInstance(response.context['form'], LabelForm)
        self.assertFalse(Label.objects.filter(name='created_label').exists())

        response = self.client.post(self.url, self.data_for_label)
        self.assertRedirects(response, reverse_lazy('labels:list'), 302)
        flash_message_test(response, _('Label created successfully'))
        self.assertTrue(Label.objects.filter(name='created_label').exists())

    def test_create_label_by_guest(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse_lazy('login'), 302)
        flash_message_test(response, _('You are not authorized'))

        self.client.post(self.url, self.data_for_label)
        self.assertFalse(Label.objects.filter(name='created_label').exists())

    def test_create_label_error(self):
        self.client.force_login(self.author)
        response = self.client.post(self.url, {})
        self.assertEquals(response.status_code, 200)
        flash_message_test(response, _('Error creating label'))


class TestUpdateLabel(TestCase):
    fixtures = ['users.json', 'statuses.json', 'labels.json', 'tasks.json']

    def setUp(self):
        self.label = Label.objects.get(name='important')
        self.data_for_update = {'name': 'updated_name'}
        self.author = User.objects.get(username='author')
        self.not_author = User.objects.get(username='not_author')
        self.url = reverse_lazy('labels:update', kwargs={'pk': self.label.pk})

    def test_update_label_success(self):
        self.client.force_login(self.author)

        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        self.assertIsInstance(response.context['form'], LabelForm)

        response = self.client.post(self.url, self.data_for_update)
        self.assertRedirects(response, reverse_lazy('labels:list'), 302)
        flash_message_test(response, _('Label updated successfully'))
        self.assertTrue(Label.objects.filter(name='updated_name').exists())

    def test_update_label_error(self):
        self.client.force_login(self.author)

        response = self.client.post(self.url, {})
        self.assertEquals(response.status_code, 200)
        flash_message_test(response, _('Label update error'))
        self.assertFalse(Label.objects.filter(name='updated_name').exists())

    def test_update_label_by_guest(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse_lazy('login'), 302)
        flash_message_test(response, _('You are not authorized'))


class TestDeleteLabel(TestCase):
    fixtures = ['users.json', 'statuses.json', 'labels.json', 'tasks.json']

    def setUp(self):
        self.author = User.objects.get(username='author')
        self.not_used_label = Label.objects.get(name='not_used')
        self.url = reverse_lazy(
            'labels:delete',
            kwargs={'pk': self.not_used_label.pk}
        )

    def test_delete_label_success(self):
        self.client.force_login(self.author)

        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)

        response = self.client.post(self.url)
        self.assertRedirects(response, reverse_lazy('labels:list'), 302)
        flash_message_test(response, _('Label deleted successfully'))
        self.assertFalse(Label.objects.filter(name='not_used').exists())

    def test_delete_label_protected_error(self):
        label_used = Label.objects.get(name='used')
        self.client.force_login(self.author)
        url = reverse_lazy('labels:delete', kwargs={'pk': label_used.pk})

        response = self.client.post(url)
        self.assertRedirects(response, reverse_lazy('labels:list'), 302)
        flash_message_test(
            response,
            _('Cannot delete label because it is in use')
        )
        self.assertTrue(Label.objects.filter(name='used').exists())

    def test_delete_label_by_guest(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse_lazy('login'), 302)
        flash_message_test(response, _('You are not authorized'))
        self.assertTrue(Label.objects.filter(name='not_used').exists())
