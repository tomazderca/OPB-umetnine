from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='domaca-stran'),
    path('about/', views.about, name='domaca-about'),
    path('1/', views.fresco, name='fresco'),
    path('2/', views.madonna, name='madonna'),
    path('artists/', views.artisti, name='artisti')
    #,path('test.txt', views.test)
]
