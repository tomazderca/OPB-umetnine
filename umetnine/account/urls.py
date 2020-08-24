from django.urls import path
from . import views


app_name = 'account'

urlpatterns = [
    path('profile', views.profile_view, name='profile'),
    path('profile/edit', views.edit_profile, name='edit_profile'),
    path('logout/', views.logout, name='logout'),
    path('list/', views.user_list, name='user_list'),
    path('myworks/', views.all_user_works, name='all_user_works'),
    path('delete/(<pk>)/', views.art_delete, name='art_delete'),
]
