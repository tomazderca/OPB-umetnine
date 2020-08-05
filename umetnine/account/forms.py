from django import forms
import datetime

# from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

# from .models import User
# from artists.models import Umetnina
from .models import UserArtwork


# ----------------------------

class RegisterForm(UserCreationForm):
    email = forms.EmailField(
                label='Email',
                widget=forms.EmailInput(attrs={'class': 'form-control'})
               )
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]


class EditProfileFrom(UserChangeForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'password',
        ]


# ----------------------------


class AddArtForm(UserArtwork):
    title = forms.CharField(
                label='title',
                widget=forms.TextInput(attrs={'class': 'form-control'}))
    year = forms.IntegerField(
                label='year',
                widget=forms.NumberInput(attrs={'class': 'form-control'}))
    style = forms.CharField(
                label='style',
                widget=forms.TextInput(attrs={'class': 'form-control'}))
    technique = forms.CharField(
                label='technique',
                widget=forms.TextInput(attrs={'class': 'form-control'}))
    medium = forms.CharField(
                label='medium',
                widget=forms.TextInput(attrs={'class': 'form-control'}))
    genre = forms.CharField(
                label='medium',
                widget=forms.TextInput(attrs={'class': 'form-control'}))

    # class Meta:
    #     model = UserArtwork
    #     fields = [
    #         'author',
    #         'title',
    #         'year',
    #         'style',
    #         'technique',
    #         'medium',
    #         'genre',
    #     ]

    def clean_year(self):
        made = self.cleaned_data.get('year')
        if 1900 < made < datetime.date.today().year:
            return made
        else:
            raise forms.ValidationError("This is not a valid year.")