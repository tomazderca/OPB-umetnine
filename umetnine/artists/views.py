from datetime import datetime
from itertools import chain

from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.db.models import Q
from .forms import CommentForm
from .models import Arts, Comments, ArtworksTags, Like
from .models import Arts, Comments, ArtworksTags, UserDescription
from django.contrib.auth.models import User
from django.views.generic import ListView, TemplateView




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

    def get_ordering(self):
        ordering = self.request.GET.get('ordering','-timestamp')
        return ordering



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


def dynamic_user_lookup_view(request, user_id):
    user_art = Arts.objects.filter(user_id=user_id)
    avatar = Arts.objects.filter(user_id=user_id).first() # trenutno zbere za avatar prvo slike #TODO
    useri = User.objects.get(id=user_id)
    user_liked = Like.objects.filter(user=useri)
    likes = 0
    for art in user_art:
        likes += Like.objects.filter(artwork=art.id).count()
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        user = None
    try:
        opis = UserDescription.objects.get(user_id=user_id)
    except UserDescription.DoesNotExist:
        opis = ''
    context = {
        'user': user,
        'user_art': user_art,
        'opis': opis,
        'avatar': avatar,
        'likes': likes,
        'user_liked': user_liked,
        'user_id': user_id
    }
    return render(request, 'artists/user.html', context)


def dynamic_artwork_lookup_view(request, user_id, artwork_id):
    try:
        art = Arts.objects.get(user_id=user_id, id=artwork_id)
    except Arts.DoesNotExist:
        raise Http404("No such artwork!")
    user = request.user
    comments = Comments.objects.filter(artwork_id=artwork_id).order_by('-timestamp')
    user_art = Arts.objects.filter(user_id=user_id).order_by('-likes').exclude(id=artwork_id)[:20]
    tagi = ArtworksTags.objects.filter(artwork_id=artwork_id)
    useri = User.objects.get(id=user_id)
    user_liked = Like.objects.filter(user=useri)
    art_liked = Like.objects.filter(artwork=art)
    liked_arts = Like.objects.filter(user__in=([lajker.user for lajker in art_liked])).distinct('artwork')[:20]


    liked = None
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
                       'num_likes': num_likes,
                       'user_liked': user_liked,
                       'art_liked': art_liked,
                       'liked_arts': liked_arts
                       }
        else:  # ne mores komentirati, ce nisi prijavljen
            context = {'art': art,
                       'form': CommentForm(),
                       'artwork_id': artwork_id,
                       'comments': comments,
                       'user_id': user_id,
                       'user_art': user_art,
                       'tagi': tagi,
                       'num_likes': num_likes,
                       'user_liked': user_liked,
                       'art_liked': art_liked,
                       'liked_arts': liked_arts
                       }
    else:  # request je get
        context = {'art': art,
                   'form': CommentForm(),
                   'artwork_id': artwork_id,
                   'comments': comments,
                   'user_id': user_id,
                   'user_art': user_art,
                   'tagi': tagi,
                   'num_likes': num_likes,
                   'liked': liked,
                   'user_liked': user_liked,
                   'art_liked': art_liked,
                   'liked_arts': liked_arts
                   }
    if art.user_id.id == user_id:
        return render(request, 'artists/artwork.html', context)
    else:
        return HttpResponseNotFound('<h1>Page was found</h1>')

def search(request):
    template = 'artists/search.html'
    query = request.GET.get('q', None)
    if query is not None and query !='':
        art = Arts.objects.filter(Q(title__icontains=query) | Q(description__contains=query)).order_by('likes')
        artist = User.objects.filter(Q(username__icontains=query))
        art_by_user = Arts.objects.filter(user_id__in=([umet.id for umet in artist])).order_by('likes')
        return render(request, template, {'art': art, 'artists': artist, 'artby':art_by_user})
    return redirect(request.META.get('HTTP_REFERER', '/'))