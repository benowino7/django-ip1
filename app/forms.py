from django import forms
from app.models import Album#not neccessary here

class NewsLetterForm(forms.Form):
    your_name = forms.CharField(label='First Name',max_length=30)
    email = forms.EmailField(label='Email')

class AlbumForm(forms.ModelForm):#allowing uploading images as a zip to be in the album detail and it is not a must*

    zip = forms.FileField(required=False)