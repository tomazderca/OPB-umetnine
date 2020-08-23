from django.shortcuts import render
from .models import Arts
from django.contrib.auth.models import User

#
# def home(request):
#     return HttpResponse('<h1>Domaca stran</h1>')
#
#
# def about(request):
#     return HttpResponse('<h1>Artists About</h1>')

def uporabniki(request):
    context = {
        'users': User.objects.all(),
        'artworks': Arts.objects.all()
    }
    return render(request, 'artists/uporabniki.html', context)
