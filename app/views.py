#!/usr/bin/env python
# -*- coding: utf-8 -*-  
from django.shortcuts import render
from django.http import HttpRequest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import DetailView
from .email import send_welcome_email
from app.models import Album, AlbumImage

def gallery(request):
    list = Album.objects.filter(is_visible=True).order_by('-created')
    paginator = Paginator(list, 10)

    page = request.GET.get('page')
    try:
        albums = paginator.page(page)
    except PageNotAnInteger:
        albums = paginator.page(1) # If page is not an integer, deliver first page.
    except EmptyPage:
        albums = paginator.page(paginator.num_pages) # If page is out of range (e.g.  9999), deliver last page of results.

    return render(request, 'gallery.html', { 'albums': list })

def newsletter(request):
    name = request.POST.get('your_name')
    email = request.POST.get('email')

    recipient = NewsLetterRecipients(name=name, email=email)
    recipient.save()
    send_welcome_email(name, email)
    data = {'success': 'You have been successfully added to mailing list'}
    return JsonResponse(data)

class AlbumDetail(DetailView):
     model = Album

     def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(AlbumDetail, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the images
        context['images'] = AlbumImage.objects.filter(album=self.object.id)
        return context
def search_results(request):

    if 'album' in request.GET and request.GET["album"]:
        search_term = request.GET.get("album")
        searched_albums = Album.search_by_title(search_term)
        message = f"{search_term}"

        return render(request, 'search.html',{"message":message,"albums": searched_albums})

    else:
        message = "You haven't searched for any term"
        return render(request, 'search.html',{"message":message})


def handler404(request, exception):
    assert isinstance(request, HttpRequest)
    return render(request, 'handler404.html', None, None, 404)