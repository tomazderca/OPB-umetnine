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



#
# class ArtworkLikes(models.Model):
#     artwork_id = models.ForeignKey(Arts, on_delete=models.CASCADE)
#     user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     likes = models.IntegerField()
    # likes = models.ManyToManyField('User', blank=True, related_name='artwork_likes')
    #
    # def __str__(self):
    #     return str(self.artwork_id) + " liked by: " + str(self.likes)
    #
    # def get_api_like_url(self):
    #     return reverse("artists:like-api-toggle", kwargs={'artwork_id': self.artwork_id})


# --------------------------------------- staro, pustil zato, da mi ne javlja errorjev


class Umetnik(models.Model):
    name = models.CharField(max_length=100)
    year_of_birth = models.DateField('birth')
    year_of_death = models.DateField('death')
    nationality = models.CharField(max_length=200)
    group = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Stili(models.Model):
    id = models.IntegerField(primary_key=True, null=False)
    stil = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.stil


class Umetnina(models.Model):
    title = models.CharField(max_length=100)
    year = models.IntegerField(null=True, validators=[MaxValueValidator(timezone.now().year)])
    author = models.ForeignKey(Umetnik, on_delete=models.CASCADE)
    style = models.CharField(max_length=200)
    technique = models.CharField(max_length=200)
    medium = models.CharField(max_length=200)

    def __str__(self):
        return self.title
