import os, shutil, sys
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from notification.models import NotificationPreference
# Create your models here.
from utilities.common import isValidPhone



def validate_phone(value):
    if not isValidPhone(value): 
        raise ValidationError(
            "%(value)s is not valid phone number",
            params={"value": value},
        )

class User(AbstractUser):
    phone = models.PositiveBigIntegerField(validators=[validate_phone], null = True, blank=True)
    phone_verified = models.BooleanField(default=False)
    image = models.ImageField(upload_to='media/', null=True, blank=True)
    notification = models.BooleanField(default=True)
    deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    pass

    def __str__(self):
        return f"{self.username}"
    

class LoginHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uuid = models.CharField(max_length=255, null=True)
    fcm_token = models.TextField(default='')
    os = models.CharField(max_length=255, null=True)
    os_version = models.CharField(max_length=255, null=True)
    app_version = models.CharField(max_length=255, null=True)
    device = models.CharField(max_length=255, null=True)
    device_model = models.CharField(max_length=255, null=True)
    social_provider = models.CharField(max_length=255, null=True)
    is_dashbaord_login = models.BooleanField(default=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    if created:
        NotificationPreference.objects.create(user = instance)
   
