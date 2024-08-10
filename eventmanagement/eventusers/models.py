from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUsers(AbstractUser):
    mobile_number = models.CharField(max_length=15, blank=True, null=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True,
        verbose_name='groups',
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set_permissions',
        blank=True,
        verbose_name='user permissions',
    )