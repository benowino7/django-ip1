#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import uuid
from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit
from tinymce.models import HTMLField
import datetime as dt
from django.contrib.auth.models import User

class Album(models.Model):
    title = models.CharField(max_length=60)
    editor = models.ForeignKey(User,on_delete=models.CASCADE)
    description = models.TextField(max_length=700)
    thumb = ProcessedImageField(upload_to='albums', processors=[ResizeToFit(500)], format='JPEG', options={'quality': 90})
    tags = models.CharField(max_length=30)
    is_visible = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=60, unique=True)
    #def get_absolute_url(self):
    #    return reverse('album', kwargs={'slug':self.slug})
    @classmethod
    def search_by_title(cls,search_term):
        app = cls.objects.filter(title__icontains=search_term)
        return app
    def __unicode__(self):
        return self.title
    

class tags(models.Model):
    name = models.CharField(max_length =30)

    def __str__(self):
        return self.name
        
class AlbumImage(models.Model):
    image = ProcessedImageField(upload_to='albums', processors=[ResizeToFit(1280)], format='JPEG', options={'quality': 60})
    thumb = ProcessedImageField(upload_to='albums', processors=[ResizeToFit(500)], format='JPEG', options={'quality': 70})
    album = models.ForeignKey('album', on_delete=models.PROTECT)
    alt = models.CharField(max_length=255, default=uuid.uuid4)
    created = models.DateTimeField(auto_now_add=True)
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    slug = models.SlugField(max_length=71, default=uuid.uuid4, editable=False)

class NewsLetterRecipients(models.Model):
    name = models.CharField(max_length = 30)
    email = models.EmailField()

class Editor(models.Model):
    first_name = models.CharField(max_length =30)
    last_name = models.CharField(max_length =30)
    email = models.EmailField()
    phone_number = models.CharField(max_length = 10,blank =True)

    def __str__(self):
        return self.first_name
    class meta:
        ordering =['name']
    
    def save_editor(self):
        self.save()