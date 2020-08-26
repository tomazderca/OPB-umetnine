from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import CommentForm
from .models import Arts, Comments, ArtworksTags, Like
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView


def uporabniki(request):
    context = {
        'users': User.objects.all(),
        'artworks': Arts.objects.all()
    }
    return render(request, 'artists/uporabniki.html', context)


def art_like(request, user_id, artwork_id):
    art_to_like = get_object_or_404(Arts, pk=artwork_id)
    user_that_likes = get_object_or_404(User, id=user_id)
    try:
        art_to_like.likes += 1
        art_to_like.save()
        Like.objects.create(artwork=art_to_like, user=user_that_likes)
        print("lajkal smo :", Like.objects.all())
    finally:
        return redirect("/{}/{}".format(user_id, artwork_id))


class PostListView(ListView):
    model = Arts
    template_name = 'artists/uporabniki.html'
    context_object_name = 'artworks'
    ordering = ['-timestamp']
    paginate_by = 9


# def dynamic_artwork_lookup_view(request, id):
#     art = Arts.objects.get(id=id)
#     comments = Comments.objects.filter(artwork_id=id)
#     if request.method == 'POST':
#         form = CommentForm(request.POST)
#         if form.is_valid() and request.user.is_authenticated:
#             new_comment = form.save(commit=False)
#             new_comment.timestamp = datetime.now()
#             new_comment.artwork_id = art
#             new_comment.user_id = request.user
#             new_comment.save()
#             context = {'art': art, 'id': id, 'form': CommentForm(), 'new_comment': new_comment, 'comments': comments}
#             # return render(request, 'artists/artwork.html', context)
#         else:  # ne mores komentirati, če nisi prijavljen
#             context = {'art': art, 'form': CommentForm(), 'id': id, 'comments': comments}
#     else:  # request je get
#         context = {'art': art, 'form': CommentForm(), 'id': id, 'comments': comments}
#     return render(request, 'artists/artwork.html', context)


# testiranje -------------------------------------------------
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User


class ArtworkLikeAPIToggle(APIView):
    print("poklicala sem API funkcijo")

    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, artwork_id=None):
        print("GET: ", artwork_id)
        print("moj id: ", self.request.user.id)
        obj = get_object_or_404(Arts, artwork_id=artwork_id)
        # obj = ArtworkLikes.objects.get(artwork_id=artwork_id)
        print("obj_ ", obj)
        # url_ = obj.get_absolute_url()
        user = self.request.user
        print("user: ", user)
        updated = False
        liked = False
        print("midpoint")
        if user.is_authenticated:
            print("kul, si vpisana")
            print(obj.likes)
            # print(obj.likes.all())
            print("do tu ne pride")
            if user in obj.likes.all():
                liked = False
                obj.likes.remove(user)
            else:
                obj.likes.add(user)
                liked = True
            updated = True
        data = {
            "updated": updated,
            "liked": liked
        }
        return Response(data)


from rest_framework.decorators import api_view


@api_view(['GET'])
def artwork_like_API_toggle(request, artwork_id):
    print("zagnala sm funkcijo")
    if request.method == "GET":
        print("GET: ", artwork_id)
        print("moj id: ", request.user.id)
        obj = get_object_or_404(Arts, id=artwork_id)
        user = request.user
        liked = False
        if user.is_authenticated:
            if Like.objects.filter(artwork=obj, user=user).exists():
                # ce je sliko ze likal, ponovni pritisk like iznici:
                liked = False
                Like.objects.filter(artwork=obj, user=user).delete()
            else:
                # dodam nov like v bazo
                liked = True
                Like.objects.create(artwork=obj, user=user)
        num_likes = Like.objects.filter(artwork=artwork_id).count()
        data = {
            "liked": liked,
            "num_likes": num_likes
        }
        return Response(data)
    return Response({"message": "error"})


# testiranje -------------------------------------------------


def dynamic_user_lookup_view(request, id):
    user = User.objects.get(id=id)
    context = {
        'user': user
    }
    return render(request, 'artists/user.html', context)


def dynamic_artwork_lookup_view(request, user_id, artwork_id):
    art = Arts.objects.get(id=artwork_id)
    user = User.objects.get(id=user_id)
    comments = Comments.objects.filter(artwork_id=artwork_id).order_by('-timestamp')
    user_art = Arts.objects.filter(user_id=user_id).order_by('-likes')[:9]
    tagi = ArtworksTags.objects.filter(artwork_id=artwork_id)
    liked = Like.objects.filter(artwork=art, user=user)
    num_likes = Like.objects.filter(artwork=artwork_id).count()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
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
                       'liked': liked,
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
                   'liked': liked,
                   'num_likes': num_likes
                   }
    return render(request, 'artists/artwork.html', context)
