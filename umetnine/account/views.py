from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse
# from django.views.generic import CreateView, TemplateView
from datetime import datetime

from artists.forms import NewArtForm, TagForm
from artists.models import ArtworksTags, Tags, Arts
from .forms import RegisterForm, EditProfileFrom, AddArtForm

# Create your views here.
from .models import UserArtwork


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            login(request, new_user)
            return redirect('/about')
    else:
        form = RegisterForm()

    return render(request, 'account/register.html', {'form': form})


def user_list(request):
    queryset = User.objects.all()  # list of objects
    return render(request, 'account/userList.html', {'object_list': queryset})


def all_user_works(request):
    queryset = Arts.objects.filter(user_id=request.user.id)  # list of objects
    context = {'object_list': queryset, 'username': request.user.username}
    return render(request, 'account/all_user_works.html', context)


def profile(request):
    if not request.user.is_authenticated:
        html = "<h1>You are not logged in.</h1><a href='/login'>Log in.</a>"
        return HttpResponse(html)
    # za vpisane uporabnike pripravim pravi view
    queryset = UserArtwork.objects.all()  # list of objects
    if request.method == "POST":
        form = AddArtForm(request.POST)
        if form.is_valid():
            new_art = form.save(commit=False)
            new_art.author = request.user.username
            new_art.save()
            context = {'form': AddArtForm(), 'new_art': new_art, 'object_list': queryset}
            return render(request, 'account/profile.html', context)
        else:
            print("zajebu")
            return render(request, 'account/profile.html', {'form': AddArtForm()})
    else:  # request je get
        form = AddArtForm()
        context = {'object_list': queryset, 'form': form}
    return render(request, 'account/profile.html', context)


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
                new_tag = Tags.objects.create(tag=tg)
                ArtworksTags.objects.create(tag_id=new_tag, artwork_id=new_art)
            context = {'form': NewArtForm(), 'new_art': new_art, "form2": form2}
            return render(request, 'account/profile.html', context)
        else:
            return render(request, 'account/profile.html', {'form': NewArtForm(), "form2": TagForm()})
    else:  # request je get
        form = NewArtForm()
        form2 = TagForm()
        context = {'form': form, "form2": form2}
    return render(request, 'account/profile.html', context)


def edit_profile(request):
    if not request.user.is_authenticated:
        html = "<h1>You are not logged in.</h1><a href='/login'>Log in.</a>"
        return HttpResponse(html)
    # za vpisane uporabnike pripravim pravi view
    if request.method == 'POST':
        form = EditProfileFrom(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/user/profile')
    else:
        form = EditProfileFrom(instance=request.user)
        context = {'form': form}
        return render(request, 'account/edit_profile.html', context)

    return render(request, 'account/edit_profile.html', {})


def logout(request):
    return render(request, 'account/logout.html', {})

# ------------------------------
