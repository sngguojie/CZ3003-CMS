from django.conf.urls import url
from CMSIncident.views import *

urlpatterns = [
    # create
    url(r'^create/$', create ,name='create'),
    # read
    url(r'^read/$', read ,name='read'),
    # update
    url(r'^update/$', update ,name='update'),
    # delete
    url(r'^delete/$', delete ,name='delete'),
    # list
    url(r'^list/$', CMSIncident.views.list ,name='list'),
    
]