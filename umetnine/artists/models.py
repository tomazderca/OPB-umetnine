from django.contrib.auth.models import User
from django.db import models
from django.conf import settings

from django.core.validators import MaxValueValidator
from django.urls import reverse
from django.utils import timezone


# Create your models here.


class Arts(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, unique=False)
    title = models.CharField(max_length=100)
    description = models.TextField(unique=False, null=False, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    url = models.URLField()
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class UserDescription(models.Model):
    user_id = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.TextField(unique=False, null=False, blank=True)

    def __str__(self):
        return self.description


class Like(models.Model):
    artwork = models.ForeignKey(Arts, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user) + " likes " + str(self.artwork)


class Comments(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    artwork_id = models.ForeignKey(Arts, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    content = models.CharField(max_length=1000)

    def __str__(self):
        return self.content


class Tags(models.Model):
    tag = models.CharField(max_length=200)

    def __str__(self):
        return self.tag


class ArtworksTags(models.Model):
    artwork_id = models.ForeignKey(Arts, on_delete=models.CASCADE)
    tag_id = models.ForeignKey(Tags, on_delete=models.CASCADE)
