from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# Create your models here.


class User(AbstractUser):
    followings = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followers', blank=True)
    genres = models.CharField(max_length=2000, default="0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0")
    # genres = models.ManyToManyField()
    def __str__(self):
        return self.username
