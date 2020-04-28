from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='artists-home'),
    path('about/', views.about, name='artists-about'),
]
