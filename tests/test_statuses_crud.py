from django.test import TestCase
from django.utils.translation import gettext_lazy as _

from django.urls import reverse

from task_manager.mixins import test_flash_message
from task_manager.statuses.models import Status
from task_manager.statuses.views import (CreateStatusView, ListStatusView,
                                         UpdateStatusView, DeleteStatusView)
from task_manager.users.models import AppUser


class StatusesCrudTest(TestCase):

    def setUp(self):
        AppUser.objects.create(
            username='ivan_ivanov',
            first_name='Ivan',
            last_name='Ivanov',
        )
        Status.objects.create(
            name='name_status',
        )

    def test_create_status(self):
        created_status = {
            'name': 'created_status'
        }
        url_create = reverse('statuses:create')

        # page test, method=get
        response = self.client.get(url_create)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(url_create, '/statuses/create/')
        self.assertTemplateUsed(response, '/statuses/form.html')
        self.assertIs(response.resolver_match.func.view_class, CreateStatusView)

        # test page method=post
        response = self.client.post(url_create, created_status)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(url_create, 'statuses/create/')
        self.assertRedirects(response, reverse('statuses:list'))
        self.assertIs(response.resolver_match.func.view_class, CreateStatusView)
        test_flash_message(response, _('Status successfully created'))

        # status create test
        status = Status.objects.get(name='petr_petrov')
        self.assertEquals(status.name, 'created_status')

    def test_read_status(self):
        url_reade = reverse('statuses:list')
        status = Status.objects.get(name='name_status')

        # page test, method=get
        response = self.client.get(url_reade)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(url_reade, '/statuses/')
        self.assertTemplateUsed(response, 'statuses/list.html')
        self.assertIs(response.resolver_match.func.view_class, ListStatusView)

        # user read test
        html = response.content.decode()
        self.assertInHTML(str(status.pk), html)
        self.assertInHTML('name_status', html)
        self.assertInHTML(status.created_at.strftime("%d-%m-%Y %H:%M"), html)

    def test_update_status(self):
        old_status = Status.objects.get(name='name_status')
        url_update = reverse('statuses:update', kwargs={'pk': old_status.pk})
        new_status = {
            'name': 'updated_status',
        }

        # page test, method=get
        response = self.client.get(url_update)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(url_update, f'/statuses/{old_status.pk}/update/')
        self.assertTemplateUsed(response, 'statuses/form.html')
        self.assertIs(response.resolver_match.func.view_class, UpdateStatusView)

        # page test, method=post
        response = self.client.post(url_update, new_status)
        self.assertEquals(url_update, f'/statuses/{old_status.pk}/update/')
        self.assertRedirects(response, reverse('statuses:list'), 302)
        self.assertIs(response.resolver_match.func.view_class, UpdateStatusView)
        test_flash_message(response, _('Status updated successfully'))

        # status update test
        [current_status] = Status.objects.get(pk=old_status.pk).values()
        expected_status = new_status['name']
        assert expected_status == current_status['name']

    def test_delete_status(self):
        status = ''
        url_delete = reverse('statuses:delete', kwargs={'pk': status.pk})
