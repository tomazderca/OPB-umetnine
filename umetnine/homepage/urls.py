from django.urls import path
from . import views

app_name = 'homepage'

urlpatterns = [
    path('', views.home, name='homepage'),
    path('about/', views.about, name='about'),
    path('1/', views.fresco, name='fresco'),
    path('2/', views.madonna, name='madonna'),
    path('artists/', views.artisti, name='artisti'),
    path('test/', views.test, name='test'),

    path('<int:pk>/', views.DetailView.as_view(), name='detail'),

    #,path('test.txt', views.test)
]
