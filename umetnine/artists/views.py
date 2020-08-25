from django.shortcuts import render, redirect, get_object_or_404
from .models import Arts
from django.contrib.auth.models import User
from django.views.generic import ListView


def uporabniki(request):
    context = {
        'users': User.objects.all(),
        'artworks': Arts.objects.all()
    }
    return render(request, 'artists/uporabniki.html', context)


def art_like(request, id):
    art_to_like = get_object_or_404(Arts, pk=id)
    try:
        art_to_like.likes += 1
        art_to_like.save()
    finally:
        context = {
            'art': art_to_like,
            'id': id,
        }
        return render(request, 'artists/artwork.html', context)


class PostListView(ListView):
    model = Arts
    template_name = 'artists/uporabniki.html'
    context_object_name = 'artworks'
    ordering = ['-timestamp']
    paginate_by = 9


def dynamic_artwork_lookup_view(request, id):
    art = Arts.objects.get(id=id)
    context = {
        'art': art,
        'id': id,
    }
    return render(request, 'artists/artwork.html', context)


def dynamic_user_lookup_view(request, id):
    user = User.objects.get(id=id)
    context = {
        'user': user
    }
    return render(request, 'artists/user.html', context)
