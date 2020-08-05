from django.core.validators import MaxValueValidator
from django.db import models
from django.utils import timezone

# Create your models here.


class UserArtwork(models.Model):
    author = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    year = models.IntegerField(validators=[MaxValueValidator(timezone.now().year)])
    technique = models.CharField(default='unspecified', max_length=100)
    medium = models.CharField(default='unspecified', max_length=100)
    style = models.CharField(default='unspecified', max_length=100)
    genre = models.CharField(default='unspecified', max_length=100)

    def __str__(self):
        return self.title

    def is_valid(self):
        return True

#
# class User(models.Model):
#     name = models.CharField(max_length=100)
#     surname = models.CharField(max_length=100)
#     email = models.EmailField(blank=True, null=True)
#     username = models.CharField(unique=True, max_length=100)
#     password = models.CharField(max_length=20)
#     first_login = models.DateTimeField(default=timezone.now)
#
#     def __str__(self):
#         return self.name + ' ' + self.surname + ' -->  ' + self.username
