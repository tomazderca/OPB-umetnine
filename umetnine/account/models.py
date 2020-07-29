from django.db import models
from django.utils import timezone

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    country = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    password = models.CharField(max_length=20)
    first_login = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.name + ' ' + self.surname
