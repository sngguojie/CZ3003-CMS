from django.conf.urls import url
import views

urlpatterns = [
    # create
    url(r'^create/$', views.create ,name='create'),
    # list
   #  url(r'^list/$', views.list ,name='list'),
    
]