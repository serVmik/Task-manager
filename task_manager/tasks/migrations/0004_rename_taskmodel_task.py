# Generated by Django 4.2.5 on 2023-09-30 12:54

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('labels', '0002_rename_labelmodel_label'),
        ('statuses', '0002_rename_statusmodel_status'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tasks', '0003_alter_taskmodel_name'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TaskModel',
            new_name='Task',
        ),
    ]
