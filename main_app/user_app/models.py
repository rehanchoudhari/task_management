from django.db import models
from django.contrib.auth.models import User
from django.utils.deconstruct import deconstructible
import os

MANAGER = 'Manager'
EMPLOYEE = 'Employee'

ROLE_LIST = [(MANAGER, 'Manager'), (EMPLOYEE, 'Employee')]

@deconstructible
class GenerateProfilePath(object):
    def __init__(self):
        pass

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        path = f'media/accounts/{instance.user.id}/images/'
        name = f'profile_image.{ext}'
        return os.path.join(path, name)
    
image_path = GenerateProfilePath()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_LIST, default=EMPLOYEE)
    image = models.FileField(upload_to=image_path, blank=True, null=True)

    def __str__(self):
        return f'{self.user.first_name} | ID_{self.id}'
