from django.contrib import admin

from .models import Umetnik, Umetnina, Stili

# Register your models here.

admin.site.register(Umetnik)
admin.site.register(Umetnina)
admin.site.register(Stili)

