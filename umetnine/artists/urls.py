from django.contrib import admin
from django.urls import path, include
from . import views
from .views import PostListView, dynamic_artwork_lookup_view, art_like, dynamic_user_lookup_view

app_name = 'artists'

urlpatterns = [
    path('', PostListView.as_view(), name='artists-uporabnik'),
    path('like/<int:user_id>/<int:artwork_id>/', art_like, name='art_like'),
    path('<int:user_id>/<int:artwork_id>/', dynamic_artwork_lookup_view, name='user-artwork'),
    path('<int:user_id>/', dynamic_user_lookup_view, name='user-user'),
]