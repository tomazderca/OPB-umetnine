from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'artists'

urlpatterns = [
    path('uporabniki/', views.uporabniki, name='artists-uporabnik')

]