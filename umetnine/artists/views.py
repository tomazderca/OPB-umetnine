from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime

from artists.forms import NewArtForm

#
# def profile_view(request):
#     if not request.user.is_authenticated:
#         html = "<h1>You are not logged in.</h1><a href='/login'>Log in.</a>"
#         return HttpResponse(html)
#     # za vpisane uporabnike pripravim pravi view
#     if request.method == "POST":
#         form = NewArtForm(request.POST)
#         if form.is_valid():
#             new_art = form.save(commit=False)
#             new_art.author = request.user.id
#             new_art.timestamp = datetime.now()
#             new_art.save()
#             context = {'form': NewArtForm(), 'new_art': new_art}
#             return render(request, 'account/profile.html', context)
#         else:
#             return render(request, 'account/profile.html', {'form': NewArtForm()})
#     else:  # request je get
#         form = NewArtForm()
#         context = {'form': form}
#     return render(request, 'account/profile.html', context)
#
