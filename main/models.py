from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# Create your models here.




class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Lab(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}'


class Data(TimeStampMixin):
    title = models.CharField(max_length=10000, blank=False)
    path = models.CharField(max_length=10000, blank=False)
    source = models.ManyToManyField(Lab, related_name='labs', blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        ordering = ['created_at']



