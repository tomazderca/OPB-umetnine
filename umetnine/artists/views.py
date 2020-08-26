from datetime import datetime

from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response


from .forms import CommentForm
from .models import Arts, Comments, ArtworksTags, Like
from django.contrib.auth.models import User
from django.views.generic import ListView


def uporabniki(request):
    context = {
        'users': User.objects.all(),
        'artworks': Arts.objects.all()
    }
    return render(request, 'artists/uporabniki.html', context)


class PostListView(ListView):
    model = Arts
    template_name = 'artists/uporabniki.html'
    context_object_name = 'artworks'
    ordering = ['-timestamp']
    paginate_by = 9


@api_view(['GET'])
def artwork_like_api_toggle(request, artwork_id):
    if request.method == "GET":
        art_to_like = get_object_or_404(Arts, id=artwork_id)
        user = request.user
        liked = False
        if user.is_authenticated:
            if Like.objects.filter(artwork=art_to_like, user=user).exists():
                # ce je sliko ze likal, ponovni pritisk like iznici:
                liked = False
                Like.objects.filter(artwork=art_to_like, user=user).delete()
                art_to_like.likes -= 1
                art_to_like.save()
            else:
                # dodam nov like v bazo
                liked = True
                Like.objects.create(artwork=art_to_like, user=user)
                art_to_like.likes += 1
                art_to_like.save()
        num_likes = Like.objects.filter(artwork=artwork_id).count()
        data = {
            "liked": liked,
            "num_likes": num_likes
        }
        return Response(data)
    return Response({"message": "error"})


def dynamic_user_lookup_view(request, id):
    user = User.objects.get(id=id)
    context = {
        'user': user
    }
    return render(request, 'artists/user.html', context)


def dynamic_artwork_lookup_view(request, user_id, artwork_id):
    art = Arts.objects.get(id=artwork_id)
    user = request.user
    comments = Comments.objects.filter(artwork_id=artwork_id).order_by('-timestamp')
    user_art = Arts.objects.filter(user_id=user_id).order_by('-likes')[:9]
    tagi = ArtworksTags.objects.filter(artwork_id=artwork_id)
    if user.is_authenticated:
        liked = Like.objects.filter(artwork=art, user=user)
    num_likes = Like.objects.filter(artwork=art).count()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid() and user.is_authenticated:
            new_comment = form.save(commit=False)
            new_comment.timestamp = datetime.now()
            new_comment.artwork_id = art
            new_comment.user_id = request.user
            new_comment.save()
            context = {'art': art,
                       'artwork_id': artwork_id,
                       'form': CommentForm(),
                       'new_comment': new_comment,
                       'comments': comments,
                       'user_id': user_id,
                       'user_art': user_art,
                       'tagi': tagi,
                       'liked': liked,
                       'num_likes': num_likes
                       }
        else:  # ne mores komentirati, ce nisi prijavljen
            context = {'art': art,
                       'form': CommentForm(),
                       'artwork_id': artwork_id,
                       'comments': comments,
                       'user_id': user_id,
                       'user_art': user_art,
                       'tagi': tagi,
                       'num_likes': num_likes
                       }
    else:  # request je get
        context = {'art': art,
                   'form': CommentForm(),
                   'artwork_id': artwork_id,
                   'comments': comments,
                   'user_id': user_id,
                   'user_art': user_art,
                   'tagi': tagi,
                   'num_likes': num_likes
                   }
    return render(request, 'artists/artwork.html', context)
