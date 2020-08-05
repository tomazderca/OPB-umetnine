from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponse
# from django.views.generic import CreateView, TemplateView


from .forms import RegisterForm, EditProfileFrom

# Create your views here.
from .models import UserArtwork


def register(request):
    if request.method == "POST":
        print('post')
        form = RegisterForm(request.POST)
        if form.is_valid():
            print('ratal ti je. zdej si vpisana')
            form.save()
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            login(request, new_user)
            return redirect('/about')
        else:
            print("neki ni vredi")
    else:
        print('request je get')
        form = RegisterForm()

    return render(request, 'account/register.html', {'form': form})


def profile(request):
    if not request.user.is_authenticated:
        html = "<h1>You are not logged in.</h1><a href='/login'>Log in.</a>"
        return HttpResponse(html)
    # za vpisane uporabnike pripravim pravi view
    if request.method == "POST":
        form = UserArtwork(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'account/profile.html', {'form': form})
    else:
        form = UserArtwork()
    return render(request, 'account/profile.html', {'form': form})


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

# ------------------------------


# # def user_list_view(request):
# #     queryset = User.objects.all()
# #     context = {
# #         'object_list': queryset
# #     }
# #     return render(request, 'account/list.html', context)
