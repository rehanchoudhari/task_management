# Generated by Django 4.2.7 on 2023-11-08 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_app', '0011_rename_project_task_project_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='projects',
            name='inprogress_task_count',
            field=models.IntegerField(default=0),
        ),
    ]
