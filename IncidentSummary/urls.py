# urls.py
from django.conf.urls import url
from IncidentSummary import views

urlpatterns = [
    # create
    url(r'^create/$', views.create ,name='create'),
    # read
    url(r'^read/$', views.read ,name='read'),
    # update
    url(r'^update/$', views.update ,name='update'),
    # delete
    url(r'^delete/$', views.delete ,name='delete'),
    # list
    url(r'^list/$', views.list ,name='list'),
    
]