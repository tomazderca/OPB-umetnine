from django.contrib import admin

from .models import Arts, Comments, Tags, ArtworksTags

# Register your models here.

admin.site.register(Arts)
admin.site.register(Comments)
admin.site.register(Tags)
admin.site.register(ArtworksTags)
