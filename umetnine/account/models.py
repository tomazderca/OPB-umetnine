from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    coubtry = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    password = models.CharField(max_length=20)

    def __str__(self):
        return self.name + ' ' + self.surname
