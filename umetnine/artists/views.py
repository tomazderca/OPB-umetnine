from datetime import datetime
from functools import reduce
from itertools import chain
import operator

from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Sum, Count
from django.views.generic import ListView
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .forms import RegisterForm, EditProfileFrom
from .forms import CommentForm, NewArtForm, TagForm, UserDescriptionForm
from .models import Arts, Comments, ArtworksTags, UserDescription, Like, Tags



def uporabniki(request):
    context = {
        'users': User.objects.all(),
        'artworks': Arts.objects.all()
    }
    return render(request, 'artists/uporabniki.html', context)


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            login(request, new_user)
            return redirect('/user/profile/')
    else:
        form = RegisterForm()

    return render(request, 'artists/register.html', {'form': form})


def user_list(request):
    queryset = User.objects.all()  # list of objects
    return render(request, 'artists/userList.html', {'object_list': queryset})


def all_user_works(request):
    queryset = Arts.objects.filter(user_id=request.user.id).order_by('-timestamp')  # list of objects
    context = {'object_list': queryset, 'user': request.user}
    return render(request, 'artists/all_user_works.html', context)


def art_delete(request, pk):
    art_to_delete = get_object_or_404(Arts, id=pk)
    try:
        art_to_delete.delete()
    finally:
        return redirect("/user/myworks")


def profile_view(request):
    if not request.user.is_authenticated:
        html = "<h1>You are not logged in.</h1><a href='/login'>Log in.</a>"
        return HttpResponse(html)
    # za vpisane uporabnike pripravim pravi view
    if request.method == "POST":
        form = NewArtForm(request.POST)
        form2 = TagForm(request.POST)
        if form.is_valid() and form2.is_valid():
            new_art = form.save(commit=False)
            new_art.user_id = request.user
            new_art.timestamp = datetime.now()
            new_art.save()
            tags_input = form2.cleaned_data['tag']
            all_tags = set(tags_input.split(", "))
            for tg in all_tags:
                if not Tags.objects.filter(tag=tg).exists():
                    # ce tak tag se ne obstaja, ga dodam v bazo
                    new_tag = Tags.objects.create(tag=tg)
                    ArtworksTags.objects.create(tag_id=new_tag, artwork_id=new_art)
            # return
            return redirect('/user/myworks/')
        else:
            return render(request, 'artists/profile.html', {'form': NewArtForm(), "form2": TagForm()})
    else:  # request je get
        form = NewArtForm()
        form2 = TagForm()
        context = {'form': form, "form2": form2}
    return render(request, 'artists/profile.html', context)


def edit_profile(request):
    if not request.user.is_authenticated:
        html = "<h1>You are not logged in.</h1><a href='/login'>Log in.</a>"
        return HttpResponse(html)
    # za vpisane uporabnike pripravim pravi view
    if request.method == 'POST':
        form = EditProfileFrom(request.POST, instance=request.user)
        form2 = UserDescriptionForm(request.POST)
        if form.is_valid() and form2.is_valid():
            # dobro je izpolnjeno, posodobim bazo
            UserDescription.objects.update_or_create(
                user_id_id=request.user.id,
                defaults={'description': form2.cleaned_data['description']}
            )
            form.save()
            return redirect('/user/profile')
        else:
            # ce formi niso dobro izpolnjeni
            form = EditProfileFrom()
            form2 = UserDescriptionForm()
    else:
        try:
            old_description = UserDescription.objects.get(user_id_id=request.user.id)
            form2 = UserDescriptionForm(instance=old_description)
        except Exception:
            form2 = UserDescriptionForm()
        form = EditProfileFrom(instance=request.user)
        context = {'form': form, 'form2': form2}
        return render(request, 'artists/edit_profile.html', context)

    return render(request, 'artists/edit_profile.html', {})


def logout(request):
    return render(request, 'artists/logout.html', {})


class PostListView(ListView):
    model = Arts
    template_name = 'artists/uporabniki.html'
    context_object_name = 'artworks'
    ordering = ['-timestamp']
    paginate_by = 15

    def get_ordering(self):
        ordering = self.request.GET.get('ordering', '-timestamp')
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


@api_view(['GET'])
def edit_comment_api(request, comment_id, new_comment):
    if request.method == "GET":
        comment_to_change = Comments.objects.get(id=comment_id)
        user = request.user
        if user.is_authenticated and user == comment_to_change.user_id:
            comment_to_change.content = new_comment
            comment_to_change.save()
            data = {
                "success": True,
                "new-comment": comment_to_change.content
            }
            return Response(data)
    return Response({"message": "error"})


def dynamic_user_lookup_view(request, user_id):
    user_art = Arts.objects.filter(user_id=user_id)
    avatar = Arts.objects.filter(user_id=user_id).first()  # TODO: trenutno zbere za avatar prvo slike
    useri = User.objects.get(id=user_id)
    user_liked = Like.objects.filter(user=useri)
    likes = 0
    for art in user_art:
        likes += art.likes
        # likes += Like.objects.filter(artwork=art.id).count()
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
        # napisem nov koment
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
    return render(request, 'artists/artwork.html', context)


def search(request):
    template = 'artists/search.html'
    query = request.GET.get('q', '')

    splitq = query.split()
    tag_qs = reduce(operator.or_, (Q(tag_id__tag__iexact=x) for x in splitq))
    title_qs = reduce(operator.and_, (Q(title__icontains=x) for x in splitq))

    if query.isspace() or query is None or query == '':
        return redirect(request.META.get('HTTP_REFERER', '/'))

    artists = User.objects.filter(Q(username__icontains=query))
    arti = Arts.objects.filter(Q(title__icontains=query) | Q(description__contains=query) | title_qs)
    art_by_user = Arts.objects.filter(user_id__in=([umet.id for umet in artists]))
    tagi = ArtworksTags.objects.filter(Q(tag_id__tag__iexact=query) | tag_qs)
    tagged_art = Arts.objects.filter(id__in=([tag.artwork_id.id for tag in tagi]))
    art = list(set(chain(arti, art_by_user, tagged_art)))

    paginator_art = Paginator(art, 20)
    art_page = request.GET.get('art_page')

    try:
        art = paginator_art.page(art_page)
    except PageNotAnInteger:
        art = paginator_art.page(1)
    except EmptyPage:
        art = paginator_art.page(paginator_art.num_pages)

    paginator_artists = Paginator(artists, 10)
    artists_page = request.GET.get('artists_page')

    try:
        artists = paginator_artists.page(artists_page)
    except PageNotAnInteger:
        artists = paginator_artists.page(1)
    except EmptyPage:
        artists = paginator_artists.page(paginator_artists.num_pages)

    art_by_user = Arts.objects.filter(user_id__in=([umet.id for umet in artists])).order_by('likes')
    art_page_obj = paginator_art.get_page(art_page)
    artists_page_obj = paginator_artists.get_page(artists_page)

    context = {'art': art,
               'artists': artists,
               'artby': art_by_user,
               'art_page_obj': art_page_obj,
               'artists_page_obj': artists_page_obj,
               'query': query,
               'art_page': art_page,
               'artists_page': artists_page,
               'tagi': tagged_art
               }

    return render(request, template, context)


def all_users(request):
    users = get_user_model().objects.annotate(
        suma=Sum('arts__likes'),
        red=Count('arts__id')
    ).order_by('username')

    paginator = Paginator(users, 20)
    page = request.GET.get('page')

    try:
        page = paginator.page(page)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    template = 'artists/all_users.html'
    context = {
        'liked': users,
        'page': page
    }
    return render(request, template, context)


def all_tags(request):
    used_tags = ArtworksTags.objects.all().distinct('tag_id__tag')
    template_name = 'artists/all_tags.html'
    context = {
        'tags': used_tags
    }
    return render(request, template_name, context)


def tag_search(request, tag_id):
    template_name = 'artists/tag_search.html'
    tag_str = Tags.objects.get(id=tag_id)
    similar_tags = Tags.objects.filter(tag=tag_str)
    tagged = ArtworksTags.objects.filter(tag_id__in=([tagid.id for tagid in similar_tags]))
    context = {
        'tagged': tagged
    }
    return render(request, template_name, context)
