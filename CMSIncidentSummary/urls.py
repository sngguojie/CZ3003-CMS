# urls.py
from django.conf.urls import url
from views import *

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
    url(r'^list/$', views.list ,name='list'),
    
]