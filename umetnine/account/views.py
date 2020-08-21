from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse
# from django.views.generic import CreateView, TemplateView


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
