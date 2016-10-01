from django.conf.urls import url
import views

urlpatterns = [
    # create
    url(r'^create/$', views.create ,name='create'),
    # read
    url(r'^read/(?P<obj_id>[0-9]+)/$', views.read ,name='read'),
    # update
    url(r'^update/(?P<obj_id>[0-9]+)/$', views.update ,name='update'),
    # delete
    url(r'^delete/$', views.delete ,name='delete'),
    # list
    url(r'^list/$', views.list ,name='list'),
    
]