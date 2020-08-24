from django.shortcuts import render
from .models import Arts
from django.contrib.auth.models import User
from django.views.generic import ListView
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

class PostListView(ListView):
    model = Arts
    template_name = 'artists/uporabniki.html'
    context_object_name = 'artworks'
    ordering = ['-timestamp']
    paginate_by = 9

def dynamic_artwork_lookup_view(request, id):
    art = Arts.objects.get(id=id)
    context = {
        'art':art
    }
    return render(request, 'artists/artwork.html', context)
