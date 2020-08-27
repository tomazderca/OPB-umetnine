from django.urls import path
from . import views

app_name = 'artists'

urlpatterns = [
    path('', views.PostListView.as_view(), name='artists-uporabnik'),
    path('<int:user_id>/<int:artwork_id>/', views.dynamic_artwork_lookup_view, name='user-artwork'),
    path('like/<int:artwork_id>/', views.artwork_like_api_toggle, name="api-like-toggle"),
    path('<int:user_id>/', views.dynamic_user_lookup_view, name='user-user'),
    path('search/', views.search, name="search")
]