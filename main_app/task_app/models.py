from django.db import models
import uuid
import os
from django.contrib.auth.models import User
from django.utils.deconstruct import deconstructible

# Create your models here.


NOT_COMPLETED = 'Not_Completed'
COMPLETED = 'Completed'

status_list = [
    (NOT_COMPLETED, 'Not_Completed'),
    (COMPLETED, 'Completed')
]

NORMAL = 'Normal'
MEDIUM = 'Medium'
HIGH = 'High'

priority_list = [
    (NORMAL, 'Normal'),
    (MEDIUM, 'Medium'),
    (HIGH, 'High')
]


@deconstructible
class GenerateAttachmentPath(object):
    def __init__(self):
        pass
    def __call__(self, instance, file_name):
        ext = file_name.split('.')[-1]
        path = f'media/task/{instance.task.id}/attachment'
        name = f'{instance.id}.{ext}'
        return os.path.join(path, name)

attachment_path = GenerateAttachmentPath()


class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project_id = models.ForeignKey('Projects', on_delete=models.CASCADE, related_name='task_within_project')
    task_summary = models.CharField(max_length=250, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey('user_app.Profile', on_delete=models.CASCADE, related_name='created_by')
    updated_by = models.ForeignKey('user_app.Profile', on_delete=models.CASCADE, related_name='updated_by')
    assign_to = models.ForeignKey('user_app.Profile', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    priority = models.CharField(choices=priority_list, default=NORMAL, max_length=20)
    status = models.CharField(choices=status_list, default=NOT_COMPLETED, max_length=30)
    due_date = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f'assign to _{self.assign_to} | created_by {self.created_by} | {self.id}'
    

class Projects(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project_name = models.CharField(max_length=120, null=False, blank=False)
    project_description = models.TextField()
    created_by = models.ForeignKey('user_app.Profile', on_delete=models.SET_NULL, blank=True, null=True)
    total_task_count = models.IntegerField(default=0)
    completed_task_count = models.IntegerField(default=0)
    not_completed_task_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(choices=status_list, default=NOT_COMPLETED, max_length=30)

    def __str__(self):
        return f'Created_by_{self.created_by} | {self.id} | Project_{self.project_name}'
    

class Attachment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to=attachment_path)
    task = models.ForeignKey('task_app.Task', on_delete=models.CASCADE, related_name='attachment')

    def __str__(self):
        return f'{self.id}'