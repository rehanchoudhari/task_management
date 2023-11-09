# Generated by Django 4.2.7 on 2023-11-07 09:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0003_initial'),
        ('task_app', '0008_alter_projects_created_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projects',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='user_app.profile'),
        ),
    ]