from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='domaca-stran'),
    path('about/', views.about, name='domaca-about'),
]
