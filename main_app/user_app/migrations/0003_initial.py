# Generated by Django 4.2.7 on 2023-11-04 13:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import user_app.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user_app', '0002_delete_customuser'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('Manager', 'Manager'), ('Employee', 'Employee')], default='Employee', max_length=20)),
                ('image', models.FileField(blank=True, null=True, upload_to=user_app.models.GenerateProfilePath())),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]