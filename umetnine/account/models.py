from django.core.validators import MaxValueValidator
from django.db import models
from django.utils import timezone

# Create your models here.


class UserArtwork(models.Model):
    author = models.CharField(max_length=100, default='unknown')
    title = models.CharField(max_length=100)
    year = models.IntegerField(validators=[MaxValueValidator(timezone.now().year)])
    technique = models.CharField(default='unspecified', max_length=100)
    medium = models.CharField(default='unspecified', max_length=100)
    style = models.CharField(default='unspecified', max_length=100)
    genre = models.CharField(default='unspecified', max_length=100)
    source = models.CharField(default='None', max_length=300)

    def __str__(self):
        return self.title

    def is_valid(self):
        pass
