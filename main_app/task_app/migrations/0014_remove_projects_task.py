# Generated by Django 4.2.7 on 2023-11-08 12:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task_app', '0013_remove_projects_inprogress_task_count_projects_task_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projects',
            name='task',
        ),
    ]
