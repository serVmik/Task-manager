# Generated by Django 4.2.5 on 2023-09-26 08:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_alter_taskmodel_labels'),
    ]

    operations = [
        migrations.RenameField(
            model_name='taskmodel',
            old_name='descriptions',
            new_name='description',
        ),
    ]