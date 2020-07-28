from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView

from .models import User
from .forms import UserForm

# Create your views here.


# def new_user_view(request):
#     form = UserForm(request.POST or None)
#     if form.is_valid():
#         form.save()
#         form = UserForm()
# 
#     context = {
#         'form': form, 
#         'title': 'tle se vpises', 
#     }
#     return render(request, 'account/register.html', context)

class RegisterView(CreateView):
    model = User
    form_class = UserForm
    template_name = 'account/register.html'


# def user_view(request):
#    usr =
