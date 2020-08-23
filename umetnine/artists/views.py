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
    paginate_by = 10

# def uporabniki2(request):
#     users = User.objects.all()
#     artworks = Arts.objects.all()
#     paginator = Paginator(users, 10)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     return render(request, 'artists/uporabniki.html', {'page_obj': page_obj, 'users': users, 'artwor'})