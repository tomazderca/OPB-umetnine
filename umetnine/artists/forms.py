from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import User

from artists.models import Arts, Tags, Comments, UserDescription


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
            'password'
        ]
        exclude = ['password']


class TagForm(forms.ModelForm):
    tag = forms.CharField(
        label='tags',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'E. g. painting, oil, realism'}))

    class Meta:
        model = Tags
        fields = ['tag']


class CommentForm(forms.ModelForm):
    content = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Comment...',
                   'style': "text-align: left;"})
    )

    class Meta:
        model = Comments
        fields = ['content']


class UserDescriptionForm(forms.ModelForm):
    class Meta:
        model = UserDescription
        fields = ['description']


class NewArtForm(forms.ModelForm):
    title = forms.CharField(
        label='title',
        widget=forms.TextInput(attrs={'class': 'form-control'})),
    description = forms.CharField(
        label='description',
        widget=forms.TextInput(attrs={'class': 'form-control'})),
    url = forms.URLField(
        label='image source (url)',
        widget=forms.URLInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Arts
        fields = [
            'title',
            'description',
            'url'
        ]
