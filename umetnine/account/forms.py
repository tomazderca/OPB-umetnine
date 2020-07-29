from django import forms
import datetime

from .models import User


class UserForm(forms.ModelForm):
    name = forms.CharField(
                label='Name', 
                widget=forms.TextInput(attrs={'class': 'form-control', 'name':'name'})
                )
    surname = forms.CharField(
                label='Surname',
                widget=forms.TextInput(attrs={'class': 'form-control'})
                )
    email = forms.EmailField(
                label='Email',
                widget=forms.EmailInput(attrs={'class': 'form-control'})
                )
    country = forms.CharField(
                label='Country',
                widget=forms.TextInput(attrs={'class': 'form-control'})
                )
    password1 = forms.CharField(
                label='Password',
                widget=forms.PasswordInput(
                    attrs={
                        'placeholder': 'password',
                        'class': 'form-control',
                        }
                    )
                )
    password2 = forms.CharField(
                label='Password',
                widget=forms.PasswordInput(
                    attrs={
                        'placeholder': 'repeat password',
                        'class': 'form-control',
                        }
                    )
                )

    class Meta:
        model = User
        fields = [
            'name',
            'surname',
            'email',
            'country',
            'password1',
            'password2',
        ]

    def clean_born(self, *args, **kwargs):
        born = self.cleaned_data.get('born')
        if 1900 < born < datetime.date.today().year:
            return born
        else:
            raise forms.ValidationError("This is not a valid year.")

    def clean_name(self):
        data = self.cleaned_data.get('name')
        if not 'B' in data:
            print("napaka v imenu - manjka B")
            raise forms.ValidationError('to ni pravo ime.')
        return data

    def clean(self, *args, **kwargs):
        cleaned_data = super().clean()
        print(cleaned_data)
        p1 = cleaned_data.get('password1')
        p2 = cleaned_data.get('password2')
        if (not p1 == p2) and p1 and p2:
            print("----NISO PRAVA GESLA")
            raise forms.ValidationError('Passwords do not match.')



class UserLoginForm(forms.ModelForm):
    email = forms.EmailField(
                label='Email',
                widget=forms.EmailInput(attrs={'class': 'form-control'})
                )
    password1 = forms.CharField(
                label='Password',
                widget=forms.PasswordInput(
                    attrs={
                        'placeholder': 'password',
                        'class': 'form-control',
                        }
                    )
                )

    class Meta:
        model = User
        fields = [
            'email',
            'password1',
        ]
