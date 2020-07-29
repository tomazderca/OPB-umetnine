from django.urls import path
from . import views


#app_name = 'account'

urlpatterns = [
    path('', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('data/', views.data_view, name='login'),
    path('data/', views.DataView.as_view(), name='login'),
    path('list/', views.user_list_view, name='list'),
]
