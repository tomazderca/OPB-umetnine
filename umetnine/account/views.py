from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, TemplateView

from .models import User
from .forms import UserForm, UserLoginForm

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


class LoginView(CreateView):
    model = User
    form_class = UserLoginForm
    template_name = 'account/login.html'


class DataView(TemplateView):    
    template_name = 'account/data.html'

    def get(self, request):
        form = UserForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            surname = form.cleaned_data['surname']
            country = form.cleaned_data['country']
            mail = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            
            form.save()
        
        context = {
            'form': form,
            'name': name,
            'surname': surname,
            'mail': mail,
            'country': country,
            'password': password,
            'password2': password2,
        }
        return render(request, self.template_name, context)


def data_view(request):
    form = UserForm(request.GET)
    #variable= form.cleaned_data['name']
    #print(variable)
    context={
        'name': request.GET.get('name'),
        'surname': request.GET.get('surname'),
        'mail': request.GET.get('Email'),
        'country': request.GET.get('Country'),
        'password': request.GET.get('Password'),
        #'data': variable,
        }
    return render(request, 'account/data.html', context)


def user_list_view(request):
    queryset = User.objects.all()
    context = {
        'object_list': queryset
    }
    return render(request, 'account/list.html', context)
