from django.contrib import admin
from django.urls import path, include
from . import views
from .views import PostListView, dynamic_artwork_lookup_view

app_name = 'artists'

urlpatterns = [
    path('', PostListView.as_view(), name='artists-uporabnik'),
    path('artworks/<int:id>/', dynamic_artwork_lookup_view, name='artwork')


]