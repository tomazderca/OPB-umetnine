from django.contrib import admin
from django.urls import path, include
from . import views
from .views import PostListView

app_name = 'artists'

urlpatterns = [
    path('uporabniki/', PostListView.as_view(), name='artists-uporabnik')

]