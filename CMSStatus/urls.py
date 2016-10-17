from django.conf.urls import url
import views

urlpatterns = [
    # read
    url(r'^read/(?P<obj_id>[0-9]+)/$', views.read ,name='read'),
    # update
    url(r'^update/(?P<obj_id>[0-9]+)/$', views.update ,name='update'),
]