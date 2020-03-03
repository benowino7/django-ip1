from django.conf.urls import url #url handler
from . import views # will set the url of spesific views which contains the template to be viewed
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    url(r'^search/', views.search_results, name='search_results')#path for searched resultd
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) #adding a static path of the root media