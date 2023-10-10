import logging

from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from task_manager.users.models import UserModel

from task_manager.tests.testing_functions import flash_message_test
from task_manager.statuses.models import Status
from task_manager.statuses.views import (
    CreateStatusView,
    ListStatusesView,
    UpdateStatusView,
    DeleteStatusView,
)

logging.getLogger('main_log')


class StatusesCrudTest(TestCase):

    def setUp(self):
        UserModel.objects.create(
            username='ivan_ivanov',
            first_name='Ivan',
            last_name='Ivanov',
        )
        Status.objects.create(
            name='name_status',
        )

    def test_create_status(self):
        user = UserModel.objects.get(username='ivan_ivanov')
        created_status = {'name': 'created_status'}
        url_create = reverse('statuses:create')

        """ Test create status by an authenticated user """

        self.client.force_login(user)

        # page test, method=get
        response = self.client.get(url_create)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(url_create, '/statuses/create/')
        self.assertIs(response.resolver_match.func.view_class, CreateStatusView)

        # page test, method=post
        response = self.client.post(url_create, created_status)
        self.assertEquals(url_create, '/statuses/create/')
        self.assertRedirects(response, reverse('statuses:list'), 302)
        self.assertIs(response.resolver_match.func.view_class, CreateStatusView)
        flash_message_test(response, _('Status successfully created'))

        # status create test
        status = Status.objects.get(name='created_status')
        self.assertEquals(status.name, 'created_status')

        self.client.logout()

        """ Test try to create status by anonymous """

        response = self.client.get(url_create)
        self.assertEquals(response.status_code, 302)
        flash_message_test(response, _('Invalid action'))
        self.client.logout()
        response = self.client.post(url_create, created_status)
        self.assertEquals(response.status_code, 302)
        flash_message_test(response, _('Invalid action'))

    def test_read_statuses(self):
        url_reade = reverse('statuses:list')
        status = Status.objects.get(name='name_status')
        user = UserModel.objects.get(username='ivan_ivanov')
        self.client.force_login(user)

        # page test, method=get
        response = self.client.get(url_reade)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(url_reade, '/statuses/')
        self.assertIs(response.resolver_match.func.view_class, ListStatusesView)

        # statuses list read test
        html = response.content.decode()
        self.assertInHTML(str(status.pk), html)
        self.assertInHTML('name_status', html)
        self.assertInHTML(status.created_at.strftime("%d-%m-%Y %H:%M"), html)

    def test_update_status(self):
        old_status = Status.objects.get(name='name_status')
        url_update = reverse('statuses:update', kwargs={'pk': old_status.pk})
        updated_status = {'name': 'updated_status'}
        user = UserModel.objects.get(username='ivan_ivanov')
        self.client.force_login(user)

        # page test, method=get
        response = self.client.get(url_update)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(url_update, f'/statuses/{old_status.pk}/update/')
        self.assertIs(response.resolver_match.func.view_class, UpdateStatusView)

        # page test, method=post
        response = self.client.post(url_update, updated_status)
        self.assertEquals(url_update, f'/statuses/{old_status.pk}/update/')
        self.assertRedirects(response, reverse('statuses:list'), 302)
        self.assertIs(response.resolver_match.func.view_class, UpdateStatusView)
        flash_message_test(response, _('Status updated successfully'))

        # status update test
        [current_status] = Status.objects.filter(pk=old_status.pk).values()
        expected_status = updated_status['name']
        assert expected_status == current_status['name']

    def test_delete_status(self):
        status = Status.objects.get(name='name_status')
        user = UserModel.objects.get(username='ivan_ivanov')
        url_delete = reverse('statuses:delete', kwargs={'pk': status.pk})

        """ Test delete status by authenticated user """

        self.client.force_login(user)

        # page test, method=get
        response = self.client.get(url_delete)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(url_delete, f'/statuses/{status.pk}/delete/')
        self.assertIs(response.resolver_match.func.view_class, DeleteStatusView)

        # page test, method=post
        response = self.client.post(url_delete)
        self.assertEquals(url_delete, f'/statuses/{status.pk}/delete/')
        self.assertRedirects(response, reverse('statuses:list'), 302)
        self.assertIs(response.resolver_match.func.view_class, DeleteStatusView)
        flash_message_test(response, _('Status successfully deleted'))

        # status deletion test
        self.assertFalse(Status.objects.filter(name='name_status').exists())

        self.client.logout()

        """ Try to delete status by anonymous """

        response = self.client.get(url_delete)
        self.assertEquals(response.status_code, 302)
        flash_message_test(response, _('Only the author can delete status'))
        self.client.logout()
        response = self.client.post(url_delete)
        self.assertEquals(response.status_code, 302)
        flash_message_test(response, _('Only the author can delete status'))
