from django.urls import path
from . import views

app_name = 'artists'

urlpatterns = [
    path('', views.PostListView.as_view(), name='artists-uporabnik'),
    path('like/<int:user_id>/<int:artwork_id>/', views.art_like, name='art_like'),
    path('<int:user_id>/<int:artwork_id>/', views.dynamic_artwork_lookup_view, name='user-artwork'),
    path('like/<int:artwork_id>/', views.artwork_like_api_toggle, name="api-like-toggle"),
]