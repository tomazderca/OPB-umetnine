from django.shortcuts import render, redirect
# from django.views.generic import CreateView, TemplateView

# from django.contrib import messages


from .forms import RegisterForm

# Create your views here.


def register(request):
    if request.method == "POST":
        print('post')
        form = RegisterForm(request.POST)
        if form.is_valid():
            print('ratal ti je. zdej si vpisana')
            form.save()
            return redirect('/')
        else:
            print("neki ni vredi")
    else:
        print('request je get')
        form = RegisterForm()

    return render(request, 'account/register.html', {'form': form})



# ------------------------------

# class RegisterView(CreateView):
#     model = User
#     form_class = UserForm
#     template_name = 'account/register.html'
#
#     def post(self, request, *args, **kwargs):
#         form = UserForm(request.POST or None)
#         if form.is_valid():
#             name = form.cleaned_data['name']
#             surname = form.cleaned_data['surname']
#             username = form.cleaned_data['username']
#             mail = form.cleaned_data['email']
#             password = form.cleaned_data['password1']
#             password2 = form.cleaned_data['password2']
#
#             context = {
#                 'form': form,
#                 'name': name,
#                 'surname': surname,
#                 'mail': mail,
#                 'username': username,
#                 'password': password,
#                 'password2': password2,
#             }
#             form.save()
#             return render(request, "account/profile.html", context)
#
#         return render(request, 'account/register.html', {'form': form})
#
#
# class LoginView(CreateView):
#     model = User
#     form_class = UserLoginForm
#     template_name = 'account/login.html'
#
#     def get(self, request, *args, **kwargs):
#         print("poskusamo z: ", request.method)
#         print(request.body)
#
#     def post(self, request, *args, **kwargs):
#         print("poskusamo z: ", request.method)
#         print(request.body)
#         form = UserLoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password1']
#
#             user = authenticate(request, username=username, password=password)
#
#             if user is not None:
#                 login(request, user)
#                 print("NASLIII")
#                 return redirect('homepage')
#             else:
#                 print("NE OBSTAJAS, ZAL")
#                 messages.info(request, "User does not exist!")
#
#
# def login_page_view(request):
#     if request.method == "POST":
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)
#
#         if user is not None:
#             login(request, user)
#             print("LOGIRAN SI, jej!")
#             return redirect('homepage')
#         else:
#             messages.info(request, 'Username OR password is incorrect.')
#
#         context = {}
#         return render(request, 'account/login.html', context)
#
#
#
#
#
# class ProfileView(TemplateView):
#     template_name = 'account/profile.html'
#     form = UserForm()
#
#
# def profile_view(request):
#     form = UserForm(request.GET)
#     context={
#         'name': request.GET.get('name'),
#         'surname': request.GET.get('surname'),
#         'mail': request.GET.get('Email'),
#         'username': request.GET.get('Username'),
#         'password': request.GET.get('Password'),
#         }
#     return render(request, 'account/profile.html', context)
#
# #
# # def user_list_view(request):
# #     queryset = User.objects.all()
# #     context = {
# #         'object_list': queryset
# #     }
# #     return render(request, 'account/list.html', context)
