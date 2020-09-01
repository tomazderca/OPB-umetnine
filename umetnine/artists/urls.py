from django.urls import path
from . import views

app_name = 'artists'

urlpatterns = [
    path('', views.PostListView.as_view(), name='artists-uporabnik'),
    path('<int:user_id>/<int:artwork_id>/', views.dynamic_artwork_lookup_view, name='user-artwork'),
    path('like/<int:artwork_id>/', views.artwork_like_api_toggle, name="api-like-toggle"),
    path('editcomment/<int:comment_id>/<str:new_comment>', views.edit_comment_api, name="edit_comment_api"),
    path('<int:user_id>/', views.dynamic_user_lookup_view, name='user-user'),
    path('search/', views.search, name="search"),
    path('users/', views.all_users, name='all-users'),
    path('tags/', views.all_tags, name='all-tags'),
    path('tags/<tag_id>', views.tag_search, name='tag-search'),

    path('user/profile/', views.profile_view, name='profile'),
    path('user/profile/edit/', views.edit_profile, name='edit_profile'),
    path('user/logout/', views.logout, name='logout'),
    path('user/list/', views.user_list, name='user_list'),
    path('user/myworks/', views.all_user_works, name='all_user_works'),
    path('user/delete/(<pk>)/', views.art_delete, name='art_delete'),
]
