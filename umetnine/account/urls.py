from django.urls import path
from . import views


app_name = 'account'

urlpatterns = [
    #path('', views.RegisterView.as_view(), name='register'),
    path('', views.register, name='register'),

    #path('login/', views.LoginView.as_view(), name='login'),
    #path('login/', views.login_page_view, name='login'),

    #path('profile/', views.profile_view, name='login'),
    #path('profile/', views.ProfileView.as_view(), name='profile'),
    #path('list/', views.user_list_view, name='list'),
]
