#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from django import forms
from app.models import Album

class NewsLetterForm(forms.Form):
    your_name = forms.CharField(label='First Name',max_length=30)
    email = forms.EmailField(label='Email')

class AlbumForm(forms.ModelForm):

    zip = forms.FileField(required=False)