from django.db import models
from django.conf import settings

from django.core.validators import MaxValueValidator
from django.utils import timezone


# Create your models here.

class Arts(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    timestamp = models.DateTimeField()
    url = models.URLField()
    likes = models.IntegerField()

    def __str__(self):
        return self.title


class Comments(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    artwork_id = models.ForeignKey(Arts, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    content = models.TextField()

    def __str__(self):
        return self.content


class Tags(models.Model):
    id = models.AutoField(primary_key=True)
    tag = models.CharField(max_length=25)

    def __str__(self):
        return self.tag


class ArtworksTags(models.Model):
    artwork_id = models.ForeignKey(Arts, on_delete=models.CASCADE)
    tag_id = models.ForeignKey(Tags, on_delete=models.CASCADE)

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
