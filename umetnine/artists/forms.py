from django import forms

from artists.models import Arts, Tags


class TagForm(forms.ModelForm):
    tag = forms.CharField(
        label='tags',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'E. g. painting, oil, realism'}))

    class Meta:
        model = Tags
        fields = ['tag']


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
