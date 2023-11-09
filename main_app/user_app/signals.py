from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile
from django.core.mail import send_mail
from main_app import settings


def send_mail_to_the_user(subject, message, to):
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, to)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwarg):
    if created:
        Profile.objects.create(user=instance)
        email = instance.email
        send_mail_to_the_user('Account Info', 'Your profile is successfully created', [email])
        
