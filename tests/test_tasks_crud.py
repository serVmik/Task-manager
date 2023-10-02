import logging

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from task_manager.mixins import test_flash_message
from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.tasks.views import (
    ListTasksView,
    CreateTaskView,
    UpdateTaskView,
    # DeleteTaskView,
)

User = get_user_model()
logger = logging.getLogger('main_log')


class TaskCrudTest(TestCase):

    def setUp(self):
        # Add user author
        User.objects.create_user(
            username='user_author',
            first_name='User',
            last_name='Author',
        )
        # Add user executor
        User.objects.create_user(
            username='user_executor',
            first_name='User',
            last_name='Executor',
        )
        User.objects.create_user(
            username='new_executor',
            first_name='User_2',
            last_name='Executor_2',
        )
        Label.objects.create(
            name='test_label',
        )
        Status.objects.create(
            name='name_status',
        )
        Status.objects.create(
            name='test create',
        )
        task_data = {
            'name': 'task_name',
            'description': 'task description',
            'status': Status.objects.get(name='name_status'),
            'author': User.objects.get(username='user_author'),
            'executor': User.objects.get(username='user_executor'),
        }
        Task.objects.create(**task_data)

        task = Task.objects.get(name='task_name')
        label = Label.objects.get(name='test_label')
        task.labels.set([label])

        # Is exists
        self.assertTrue(User.objects.filter(username='user_author').exists()),
        self.assertTrue(User.objects.filter(username='user_executor').exists()),
        self.assertTrue(Task.objects.filter(name='task_name').exists())
        self.assertTrue(Label.objects.filter(name='test_label').exists())
        self.assertTrue(Status.objects.filter(name='name_status').exists()),

    def test_read_tasks(self):
        task = Task.objects.filter(name='task_name').values()
        author = User.objects.get(username='user_author')
        url = reverse('tasks:list')

        """ Test try to visit page by anonymous """

        # Add func test_visit_page_anonymous(url) !!!!!!!!!!!!!!!!!

        response = self.client.get(url)
        self.assertRedirects(response, reverse('home'), 302)
        test_flash_message(response, _('Invalid action.'))
        self.client.logout()

        """ Test visit to the page by an authorized user """

        self.client.force_login(author)
        response = self.client.get(url, *task)
        html = response.content.decode()

        # page test, method=get
        self.assertEquals(response.status_code, 200)
        self.assertEquals(url, '/tasks/')
        self.assertTemplateUsed(response, 'tasks/list.html')
        self.assertIs(response.resolver_match.func.view_class, ListTasksView)

        # html content test
        task = Task.objects.get(name='task_name')
        self.assertInHTML(str(task.pk), html)
        self.assertInHTML(task.name, html)
        self.assertInHTML(str(Status.objects.get(pk=task.status.pk)), html)
        self.assertInHTML(str(User.objects.get(pk=task.author.pk)), html)
        self.assertInHTML(str(User.objects.get(pk=task.executor.pk)), html)
        self.assertInHTML(task.created_at.strftime("%d-%m-%Y %H:%M"), html)

        # html test
        self.assertInHTML(_('Tasks'), html)
        self.assertInHTML(_('Create task'), html)
        self.assertInHTML(_('ID'), html, count=1)
        self.assertInHTML(_('Name'), html, count=1)
        self.assertInHTML(_('Status'), html)
        self.assertInHTML(_('Executor'), html)
        self.assertInHTML(_('Date of create'), html, count=1)
        self.assertInHTML(_('Edit'), html)
        self.assertInHTML(_('Delete'), html)
        # self.assertInHTML(_('Only your tasks'), html)

        # test page content filter !!!!!!!!!!!!!!!!!!

    def test_create_task(self):
        url = reverse('tasks:create')
        author = User.objects.get(username='user_author')

        self.assertTrue(Status.objects.filter(name='name_status').exists()),
        self.assertTrue(User.objects.filter(username='user_executor').exists()),
        created_task = {
            'name': 'created task',
            'description': 'created task description',
            'status': Status.objects.get(name='name_status').pk,
            'executor': User.objects.get(username='user_executor').pk,
        }

        """ Test try to create task by anonymous """

        # page test, method=get
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)
        # assert self.assertRedirects(response, reverse('home'), 302)
        test_flash_message(response, _('Invalid action.'))
        self.client.logout()
        # page test, method=post
        response = self.client.post(url)
        self.assertEquals(response.status_code, 302)
        # assert self.assertRedirects(response, reverse('home'), 302)
        test_flash_message(response, _('Invalid action.'))
        self.client.logout()

        """ Test create task by an authorized user """

        self.client.force_login(author)

        # page test, method=get
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(url, '/tasks/create/')
        self.assertTemplateUsed(response, 'tasks/form.html')
        self.assertIs(response.resolver_match.func.view_class, CreateTaskView)

        # page test, method=post,

        self.assertFalse(Task.objects.filter(name='created task').exists())
        response = self.client.post(url, created_task)
        self.assertTrue(Task.objects.filter(name='created task').exists())

        self.assertEquals(url, '/tasks/create/')
        self.assertRedirects(response, reverse('tasks:list'), 302)
        self.assertIs(response.resolver_match.func.view_class, CreateTaskView)
        test_flash_message(response, 'Task added successfully')

    def test_update_task(self):
        author = User.objects.get(username='user_author')
        new_executor = User.objects.get(username='new_executor')
        old_task = Task.objects.get(name='task_name')
        new_status = Status.objects.get(name='test create')
        updated_data = {
            'name': 'updated name',
            'description': 'updated task description',
            'status': new_status.pk,
            # 'labels': 'updated test label',
            'author': author.pk,
            'executor': new_executor.pk,
        }
        url = reverse('tasks:update', kwargs={'pk': old_task.pk})

        """ Test try to update task by anonymous """

        response = self.client.get(url)
        self.assertRedirects(response, reverse('home'), 302)
        test_flash_message(response, _('Invalid action.'))
        self.client.logout()
        response = self.client.post(url)
        self.assertRedirects(response, reverse('home'), 302)
        test_flash_message(response, _('Invalid action.'))
        self.client.logout()

        """ Test update task by an authorized user """

        self.client.force_login(author)

        # page test, method=get
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(url, f'/tasks/{old_task.pk}/update/')
        self.assertTemplateUsed(response, 'tasks/form.html')
        self.assertIs(response.resolver_match.func.view_class, UpdateTaskView)

        # page test, method=post
        response = self.client.post(url, updated_data)
        self.assertEquals(url, f'/tasks/{old_task.pk}/update/')
        self.assertRedirects(response, reverse('tasks:list'), 302)
        self.assertIs(response.resolver_match.func.view_class, UpdateTaskView)
        test_flash_message(response, _('Task successfully updated'))
        self.client.logout()

        # task update test
        [current_data] = Task.objects.filter(pk=old_task.pk).values()
        for field1, field2 in [
            ('name', 'name'),
            ('description', 'description'),
            ('status', 'status_id'),
            # ('labels', 'labels_id'),
            ('author', 'author_id'),
            ('executor', 'executor_id'),
        ]:
            self.assertEquals(updated_data[field1], current_data[field2])

        """ Task update with error """

        updated_data_error = {
            'name': 'updated name',
            'description': 'updated task description',
            'status': new_status,
        }
        self.client.force_login(author)
        response = self.client.post(url, updated_data_error)
        self.assertEquals(response.status_code, 200)
        test_flash_message(response, 'Task update error')

    # def test_delete_task(self):
    #     task = Task.objects.get(name='task name')
    #     url_delete = reverse_lazy('tasks:delete', kwargs={'pk': task.pk})
    #     print(f'+++++++++++ task.author = {task.author}')
    #     user_author = User.objects.get(username=task)
    #     user_not_author = Task.objects.get(name='ivan_ivanov')
    #
    #     """ Test try to update task by anonymous """
    #
    #     response = self.client.get(url_delete)
    #     self.assertRedirects(reverse_lazy('login'), 302)
    #     test_flash_message(response, _('Invalid action.'))
    #     self.client.logout()
    #     response = self.client.post(url_delete)
    #     self.assertRedirects(reverse_lazy('login'), 302)
    #     test_flash_message(response, _('Invalid action.'))
    #     self.client.logout()
    #
    #     """ Test delete task by an authorized user but not author"""
    #
    #     self.client.force_login(user_not_author)
    #     response = self.client.get(url_delete)
    #     self.assertRedirects(reverse_lazy('login'), 302)
    #     test_flash_message(response, _('Invalid action.'))
    #     self.client.logout()
    #     response = self.client.post(url_delete)
    #     self.assertRedirects(reverse_lazy('login'), 302)
    #     test_flash_message(response, _('Invalid action.'))
    #     self.client.logout()
    #
    #     """ Test delete task by author"""
    #
    #     self.client.force_login(user_author)
    #     response = self.client.get(url_delete)
    #     self.assertEquals(response.status_code, 200)
    #     self.assertEquals(url_delete, f'/tasks/{task.pk}/delete/')
    #     self.assertTemplateUsed(response, 'tasks/delete.html')
    #     self.assertIs(response.resolver_match.func.view_class, DeleteTaskView)
    #
    #     # page test, method=post
    #     response = self.client.post(url_delete)
    #     self.assertEquals(url_delete, f'/tasks/{task.pk}/delete/')
    #     self.assertRedirects(response, reverse_lazy('tasks:list'), 302)
    #     self.assertIs(response.resolver_match.func.view_class, DeleteTaskView)
    #     test_flash_message(response, _('Task deleted.'))
    #
    #     # task deletion test
    #     self.assertFalse(Task.objects.filter(name='test name').exists())
