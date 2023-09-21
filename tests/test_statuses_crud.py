from django.test import TestCase

from django.urls import reverse

from task_manager.statuses.views import (CreateStatusView, UpdateStatusView,
                                         DeleteStatusView)


class StatusesCrudTest(TestCase):

    def setUp(self):
        pass

    def CreateStatusTest(self):
        created_status = {}
        url_create = reverse('statuses:create')

        # test page method=get
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
        self.assertIs(response.resolver_match.func.view_class, UpdateStatusView)

    def ReadStatusTest(self):
        url_reade = reverse('statuses:list')

    def UpdateStatusTest(self):
        status = ''
        url_update = reverse('statuses:update', kwargs={'pk': status.pk})

    def DeleteStatusTest(self):
        status = ''
        url_delete = reverse('statuses:delete', kwargs={'pk': status.pk})
