import os#rendering the path in the admin 
import uuid#universal unique id
import zipfile# to allow zip handling purposes
import django_photo_gallery.settings#allows us to get the media file containing all the images
from datetime import datetime#allows track of time and date
from zipfile import ZipFile#to allow zip handling purposes

from django.contrib import admin#renders the admin
from django.core.files.base import ContentFile#each file with its content is rendered

from PIL import Image #this is a requirement which provides the imaging options(pillow)

from app.models import Album, AlbumImage,tags,Editor
from app.forms import AlbumForm

@admin.register(Album)
class AlbumModelAdmin(admin.ModelAdmin):#structuring the admin album class
    form = AlbumForm
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'thumb')
    list_filter = ('created',)

    def save_model(self, request, obj, form, change):
        if form.is_valid():#confirming validation and saving the album
            album = form.save(commit=False)
            album.modified = datetime.now()
            album.save()

            if form.cleaned_data['zip'] != None:#the fomat should be a zip file //zip file admin handler
                zip = zipfile.ZipFile(form.cleaned_data['zip'])
                for filename in sorted(zip.namelist()):

                    file_name = os.path.basename(filename)
                    if not file_name:
                        continue

                    data = zip.read(filename)#have the data as the read zip file
                    contentfile = ContentFile(data)#reading the data in the zip file and have it as contentfile

                    img = AlbumImage()#handling the image in the album containing also the zip file
                    img.album = album
                    img.alt = filename
                    filename = '{0}{1}.jpg'.format(album.slug, str(uuid.uuid4())[-13:])#give it a unique identifier
                    img.image.save(filename, contentfile)
                
                    filepath = '{0}/albums/{1}'.format(django_photo_gallery.settings.MEDIA_ROOT, filename)#points to settings in the media wherre all images are stored 
                    with Image.open(filepath) as i:
                        img.width, img.height = i.size

                    img.thumb.save('thumb-{0}'.format(filename), contentfile)
                    img.save()
                zip.close() 
            super(AlbumModelAdmin, self).save_model(request, obj, form, change)
#registering tags and editors of albums
admin.site.register(tags)
admin.site.register(Editor)
# In case image should be removed from album.
@admin.register(AlbumImage)#album image should contain a list of list of images in an album and can be filtered 
class AlbumImageModelAdmin(admin.ModelAdmin):
    list_display = ('alt', 'album')
    list_filter = ('album', 'created')