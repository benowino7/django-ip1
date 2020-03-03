import uuid #universal unique identifier
from django.db import models ##delares that this is a modal class that queries the db
from imagekit.models import ProcessedImageField #will be responsible for processing the thumb field
from imagekit.processors import ResizeToFit  #responsible for restructuring the photos
import datetime as dt #importing dates and time blueprints
from django.contrib.auth.models import User

class Album(models.Model):
    title = models.CharField(max_length=60) #defines how tittle of the album should be
    editor = models.ForeignKey(User,on_delete=models.CASCADE) # a unique connecter to othe tables
    description = models.TextField(max_length=700) #defines how the description should look like and the length of char it contains
    thumb = ProcessedImageField(upload_to='albums', processors=[ResizeToFit(500)], format='JPEG', options={'quality': 90})#provides the image field for the album
    tags = models.CharField(max_length=30)# this field is responsible for adding different tags i.e @#ben
    is_visible = models.BooleanField(default=True)# defining the view aspect to true this mode (album is visible)
    created = models.DateTimeField(auto_now_add=True)#creating the model should be true to allow submmission
    modified = models.DateTimeField(auto_now_add=True)#modifying a album should also be true
    slug = models.SlugField(max_length=60, unique=True)#shorter version of tittle
   
    @classmethod #defining a class  resposible for a search
    def search_by_title(cls,search_term):
        app = cls.objects.filter(title__icontains=search_term)
        return app #returns the object in app found
    def __unicode__(self):
        return self.title #returns the title if found
    

class tags(models.Model):
    name = models.CharField(max_length =30)

    def __str__(self):
        return self.name
        
class AlbumImage(models.Model):
    image = ProcessedImageField(upload_to='albums', processors=[ResizeToFit(1280)], format='JPEG', options={'quality': 60})#adding an image to an album
    thumb = ProcessedImageField(upload_to='albums', processors=[ResizeToFit(500)], format='JPEG', options={'quality': 70})# an alternative image for the first one
    album = models.ForeignKey('album', on_delete=models.PROTECT)#this is the connecter to the first album table
    alt = models.CharField(max_length=255, default=uuid.uuid4)#creates a universal identifier to the album model
    created = models.DateTimeField(auto_now_add=True)
    width = models.IntegerField(default=0)# sets the image width
    height = models.IntegerField(default=0)# sets the image height
    slug = models.SlugField(max_length=71, default=uuid.uuid4, editable=False)#not neccesary here

class NewsLetterRecipients(models.Model):
    name = models.CharField(max_length = 30)
    email = models.EmailField()
    #this class defines how the newletter should look like

#defines and editor for an album
class Editor(models.Model):
    first_name = models.CharField(max_length =30)
    last_name = models.CharField(max_length =30)
    email = models.EmailField()
    phone_number = models.CharField(max_length = 10,blank =True)

    def __str__(self):
        return self.first_name#returning name of the writter
    class meta:
        ordering =['name']#getting the list of editors  and ordering them by name
    
    def save_editor(self):
        self.save()