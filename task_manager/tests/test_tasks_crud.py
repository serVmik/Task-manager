from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.tasks.views import (ListTasksView, CreateTaskView,
                                      UpdateTaskView, DeleteTaskView,
                                      ShowTaskView)
from task_manager.tests.testing_functions import flash_message_test

User = get_user_model()


class ReadeTaskTest(TestCase):
    fixtures = ['users.json', 'statuses.json', 'labels.json', 'tasks.json']

    def setUp(self):
        self.task = Task.objects.filter(name='current').values()
        self.not_author = User.objects.get(username='not_author')
        self.url = reverse('tasks:list')

    def test_read_tasks_by_anonymous(self):
        response = self.client.get(self.url, *self.task)
        self.assertRedirects(response, reverse('login'), 302)
        flash_message_test(response, _('You are not authorized'))

    def test_read_tasks_by_authorized_user(self):
        self.client.force_login(self.not_author)
        response = self.client.get(self.url, *self.task)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(self.url, '/tasks/')
        self.assertTemplateUsed(response, 'tasks/list.html')
        self.assertIs(response.resolver_match.func.view_class, ListTasksView)

    def test_html_read_tasks(self):
        self.client.force_login(self.not_author)
        response = self.client.get(self.url, *self.task)
        html = response.content.decode()

        task = Task.objects.get(name='current')
        self.assertInHTML(str(task.pk), html)
        self.assertInHTML(task.name, html)
        self.assertInHTML(str(Status.objects.get(pk=task.status.pk)), html)
        self.assertInHTML(str(User.objects.get(pk=task.author.pk)), html)
        self.assertInHTML(str(User.objects.get(pk=task.executor.pk)), html)
        self.assertInHTML(task.created_at.strftime('%d-%m-%Y %H:%M'), html)

        self.assertInHTML(_('Tasks'), html)
        self.assertInHTML(_('Create task'), html, count=1)
        self.assertInHTML('ID', html, count=1)
        self.assertInHTML(_('Name'), html, count=1)
        self.assertInHTML(_('Status'), html)
        self.assertInHTML(_('Executor'), html, count=2)
        self.assertInHTML(_('Date of create'), html, count=1)
        self.assertInHTML(_('Edit'), html)
        self.assertInHTML(_('Delete'), html)


class TestCreateTaskTest(TestCase):
    fixtures = ['users.json', 'statuses.json', 'labels.json', 'tasks.json']

    def setUp(self):
        self.author = User.objects.get(username='author')
        self.status = Status.objects.get(name='new')
        executor = User.objects.get(username='executor')
        self.created_task = {
            'name': 'created task',
            'description': 'created task description',
            'status': self.status.pk,
            'executor': executor.pk,
        }
        self.task_data_error = {
            'name': 'data_error',
            'description': 'updated task description',
            'status': self.status,
        }
        self.url = reverse('tasks:create')

    def test_create_task_by_anonymous(self):
        response = self.client.post(self.url)

        self.assertRedirects(response, reverse('login'), 302)
        flash_message_test(response, _('You are not authorized'))

    def test_create_task_by_authorized_user(self):
        self.client.force_login(self.author)
        response = self.client.get(self.url)

        # page test, method=get
        self.assertEquals(response.status_code, 200)
        self.assertEquals(self.url, '/tasks/create/')
        self.assertIs(response.resolver_match.func.view_class, CreateTaskView)

        # page test, method=post
        self.assertFalse(Task.objects.filter(name='created task').exists())
        response = self.client.post(self.url, self.created_task)
        self.assertTrue(Task.objects.filter(name='created task').exists())
        self.assertEquals(self.url, '/tasks/create/')
        self.assertRedirects(response, reverse('tasks:list'), 302)
        flash_message_test(response, _('Task created successfully'))

    def test_create_task_with_error(self):
        self.client.force_login(self.author)
        response = self.client.post(self.url, self.task_data_error)
        self.assertEquals(response.status_code, 200)
        flash_message_test(response, _('Error adding task'))


class UpdateTaskTest(TestCase):
    fixtures = ['users.json', 'statuses.json', 'labels.json', 'tasks.json']

    def setUp(self):
        self.task = Task.objects.get(name='old')
        self.author = User.objects.get(username='author')
        self.not_author = User.objects.get(username='not_author')
        self.new_executor = User.objects.get(username='new_executor')
        self.new_status = Status.objects.get(name='new_status')
        self.updated_data = {
            'name': 'updated_name',
            'description': 'updated task description',
            'status': self.new_status.pk,
            # 'labels': 'updated test label',
            'author': self.author.pk,
            'executor': self.new_executor.pk,
        }
        self.task_data_error = {
            'name': 'data_error',
            'description': 'updated task description',
            'status': self.new_status,
        }

        self.url = reverse('tasks:update', kwargs={'pk': self.task.pk})

    def test_update_task_by_anonymous(self):
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('login'), 302)
        flash_message_test(response, _('You are not authorized'))

    def test_update_task_by_authorized_user(self):
        self.client.force_login(self.not_author)

        # page test, method=get
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(self.url, f'/tasks/{self.task.pk}/update/')
        self.assertIs(response.resolver_match.func.view_class, UpdateTaskView)

        # page test, method=post
        response = self.client.post(self.url, self.updated_data)
        self.assertEquals(self.url, f'/tasks/{self.task.pk}/update/')
        self.assertRedirects(response, reverse('tasks:list'), 302)
        flash_message_test(response, _('The task was successfully modified'))

    def test_updated_data_task(self):
        self.client.force_login(self.not_author)
        self.client.post(self.url, self.updated_data)

        [current_data] = Task.objects.filter(pk=self.task.pk).values()
        for field_updated_data, field_current_data in [
            ('name', 'name'),
            ('description', 'description'),
            ('status', 'status_id'),
            # ('labels', 'labels_id'),
            ('author', 'author_id'),
            ('executor', 'executor_id'),
        ]:
            self.assertEquals(
                self.updated_data[field_updated_data],
                current_data[field_current_data]
            )

    def test_update_task_with_error(self):
        self.client.force_login(self.not_author)
        response = self.client.post(self.url, self.task_data_error)
        self.assertEquals(response.status_code, 200)
        flash_message_test(response, _('Task update error'))


class DeleteTaskTest(TestCase):
    fixtures = ['users.json', 'statuses.json', 'labels.json', 'tasks.json']

    def setUp(self):
        self.author = User.objects.get(username='author')
        self.not_author = User.objects.get(username='executor')
        self.task = Task.objects.get(name='current')
        self.url = reverse('tasks:delete', kwargs={'pk': self.task.pk})

    def test_delete_task_by_anonymous(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('login'), 302)
        flash_message_test(response, _('You are not authorized'))
        self.assertTrue(Task.objects.filter(name='current').exists())

    def test_delete_task_by_not_author(self):
        self.client.force_login(self.not_author)

        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('tasks:list'), 302)
        flash_message_test(response, _('Only the author can delete task'))
        self.assertTrue(Task.objects.filter(name='current').exists())

    def test_delete_task_by_author(self):
        self.client.force_login(self.author)

        # page test, method=get
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(self.url, f'/tasks/{self.task.pk}/delete/')
        self.assertIs(response.resolver_match.func.view_class, DeleteTaskView)

        # page test, method=post
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('tasks:list'), 302)
        flash_message_test(response, _('The task was successfully deleted'))
        self.assertFalse(Task.objects.filter(name='current').exists())


class ShowTaskTest(TestCase):
    fixtures = ['users.json', 'statuses.json', 'labels.json', 'tasks.json']

    def setUp(self):
        self.author = User.objects.get(username='author')
        self.task = Task.objects.get(pk=3)
        self.url = reverse('tasks:show', kwargs={'pk': self.task.pk})

    def test_read_task(self):
        self.client.force_login(self.author)
        response = self.client.get(self.url)
        html = response.content.decode()

        self.assertEquals(response.status_code, 200)
        self.assertEquals(self.url, '/tasks/3/')
        self.assertTemplateUsed(response, 'tasks/show.html')
        self.assertIs(response.resolver_match.func.view_class, ShowTaskView)

        self.assertInHTML(_('View a task'), html)
        self.assertInHTML(_('Edit'), html)
        self.assertInHTML(_('Delete'), html)

        self.assertInHTML(self.task.name, html)
        self.assertInHTML(self.task.description, html)
        self.assertInHTML(str(self.task.author), html)
        self.assertInHTML(str(self.task.executor), html)
        self.assertInHTML(self.task.created_at.strftime('%d.%m.%Y %H:%M'), html)
        for label in self.task.labels.all():
            self.assertInHTML(label.name, html)

    def test_read_task_by_guest(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('login'), 302)
        flash_message_test(response, _('You are not authorized'))
