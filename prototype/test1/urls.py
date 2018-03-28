from django.conf.urls import url
 
from . import view, search
 
urlpatterns = [
    url(r'^$', search.search_post),
    url(r'^search-post$', search.search_post),
]
