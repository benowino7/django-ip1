from django.shortcuts import render #rendering of templates
from django.http import HttpRequest #handles the post and the get methods from the user
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger #handles massive pages
from django.views.generic import DetailView#allows detailed view for album
from .email import send_welcome_email#imports the function that allows sending  email to different recepients
from app.models import Album, AlbumImage#importing from our models the classes album and albumimage


def gallery(request):
    #desplaying the albums as list of pages containining 10 albums per page
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

#defining the newletter function
def newsletter(request):
    name = request.POST.get('your_name')
    email = request.POST.get('email')

    recipient = NewsLetterRecipients(name=name, email=email)
    recipient.save()
    send_welcome_email(name, email) #sending the newsletter email to the resipient with the details provided
    data = {'success': 'You have been successfully added to mailing list'}
    return JsonResponse(data)

class AlbumDetail(DetailView):#defines what should be presented in the detail view
     model = Album

     def get_context_data(self, **kwargs):# accept  declaring a variables and the amount within the function arguments
        # Call the base implementation first to get a context
        context = super(AlbumDetail, self).get_context_data(**kwargs)# accept  declaring a variables and the amount within the function arguments
        # Add in a QuerySet of all the images
        context['images'] = AlbumImage.objects.filter(album=self.object.id)
        return context
def search_results(request):#searching album by tittle 

    if 'album' in request.GET and request.GET["album"]:
        search_term = request.GET.get("album")#brings the album
        searched_albums = Album.search_by_title(search_term)#brings the tittle in the brought album
        message = f"{search_term}"

        return render(request, 'search.html',{"message":message,"albums": searched_albums})

    else:#define what happens if the album is not found
        message = "You haven't searched for any term"
        return render(request, 'search.html',{"message":message})


def handler404(request, exception):#handle the not found errors
    assert isinstance(request, HttpRequest)
    return render(request, 'handler404.html', None, None, 404)