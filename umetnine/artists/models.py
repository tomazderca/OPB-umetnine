from django.db import models

from django.core.validators import MaxValueValidator
from django.utils import timezone


# Create your models here.

class Umetnik(models.Model):
    name = models.CharField(max_length=100)
    year_of_birth = models.DateField('birth')
    year_of_death = models.DateField('death')
    nationality = models.CharField(max_length=200)
    group = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Umetnina(models.Model):
    title = models.CharField(max_length=100)
    year = models.IntegerField(null=True, validators=[MaxValueValidator(timezone.now().year)])
    author = models.ForeignKey(Umetnik, on_delete=models.CASCADE)
    style = models.CharField(max_length=200)
    technique = models.CharField(max_length=200)
    medium = models.CharField(max_length=200)

    def __str__(self):
        return self.title
