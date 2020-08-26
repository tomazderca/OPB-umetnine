from datetime import datetime

from django.shortcuts import render, redirect, get_object_or_404

from .forms import CommentForm
from .models import Arts, Comments, ArtworksTags
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
    try:
        art_to_like.likes += 1
        art_to_like.save()
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


def dynamic_user_lookup_view(request, id):
    user = User.objects.get(id=id)
    context = {
        'user': user
    }
    return render(request, 'artists/user.html', context)


# def all_certain_user_works(request, pk):
#     print("zdej gledam sam enga userja")
#     print(pk)
#     queryset = Arts.objects.filter(user_id=pk)  # list of objects
#     context = {'object_list': queryset, 'username': request.user.username}
#     return render(request, 'account/all_user_works.html', context)

def dynamic_artwork_lookup_view(request, user_id, artwork_id):
    art = Arts.objects.get(id=artwork_id)
    comments = Comments.objects.filter(artwork_id=artwork_id).order_by('-timestamp')
    user_art = Arts.objects.filter(user_id=user_id).order_by('-likes')[:9]
    tagi = ArtworksTags.objects.filter(artwork_id=artwork_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            new_comment = form.save(commit=False)
            new_comment.timestamp = datetime.now()
            new_comment.artwork_id = art
            new_comment.user_id = request.user
            new_comment.save()
            context = {'art': art, 'artwork_id': artwork_id, 'form': CommentForm(), 'new_comment': new_comment, 'comments': comments, 'user_id': user_id, 'user_art': user_art, 'tagi':tagi}
            # return render(request, 'artists/artwork.html', context)
        else:  # ne mores komentirati, če nisi prijavljen
            context = {'art': art, 'form': CommentForm(), 'artwork_id': artwork_id, 'comments': comments, 'user_id': user_id, 'user_art': user_art, 'tagi':tagi}
    else:  # request je get
        context = {'art': art, 'form': CommentForm(), 'artwork_id': artwork_id, 'comments': comments, 'user_id': user_id, 'user_art': user_art, 'tagi':tagi}
    return render(request, 'artists/artwork.html', context)

