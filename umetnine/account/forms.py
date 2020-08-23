from django import forms
import datetime

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

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


class AddArtForm(forms.ModelForm):
    title = forms.CharField(
                label='title',
                widget=forms.TextInput(attrs={'class': 'form-control'}))
    year = forms.IntegerField(
                label='year',
                widget=forms.NumberInput(attrs={'class': 'form-control'}))
    style = forms.ChoiceField(choices=UserArtwork.choices,
                              label='style',
                              widget=forms.Select(attrs={
                                  'class': 'form-control',
                              }))
    technique = forms.CharField(
                label='technique',
                required=False,
                widget=forms.TextInput(attrs={
                    'class': 'form-control',
                    'placeholder': "e. g. oil on canvas, print...",
                     }))
    medium = forms.CharField(
                label='medium',
                required=False,
                widget=forms.TextInput(attrs={
                    'class': 'form-control',
                    'placeholder': "e. g. acrylic, aquatint, collage...",
                    }))
    genre = forms.CharField(
                label='genre',
                required=False,
                widget=forms.TextInput(attrs={
                    'class': 'form-control',
                    'placeholder': "e. g. portrait, nude, veduta...",
                    }))
    source = forms.CharField(
                label='image source (url)',
                required=False,
                widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = UserArtwork
        fields = [
            'title',
            'year',
            'style',
            'technique',
            'medium',
            'genre',
            'source',
        ]


    def clean_year(self):
        made = self.cleaned_data.get('year')
        if 1900 < made <= datetime.date.today().year:
            return made
        else:
            raise forms.ValidationError("This is not a valid year.")
