# Generated by Django 4.2.7 on 2023-11-05 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_app', '0002_alter_attachment_id_alter_projects_id_alter_task_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='comment',
            field=models.TextField(blank=True, null=True),
        ),
    ]
