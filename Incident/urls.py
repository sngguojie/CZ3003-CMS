from django.conf.urls import url
import views
import IncidentLog.views

urlpatterns = [
    # create
    url(r'^create/$', views.create ,name='create'),
    # read
    url(r'^read/(?P<obj_id>[0-9]+)/$', views.read ,name='read'),
    # update
    url(r'^update/(?P<obj_id>[0-9]+)/$', views.update ,name='update'),
    # delete
    url(r'^delete/(?P<obj_id>[0-9]+)/$', views.delete ,name='delete'),
    # list
    url(r'^list/$', views.list ,name='list'),
    # incident log routes
    url(r'^(?P<incident_id>[0-9]+)/logs/read/$', IncidentLog.views.get_logs_for_incident, name='logs_read'),
    url(r'^(?P<incident_id>[0-9]+)/logs/create/$', IncidentLog.views.create, name='logs_create'),
    # incident call report routes
    url(r'^(?P<incident_id>[0-9]+)/callreports/create/$', views.callreports_add, name='callreports_add'),
    url(r'^callreports/create/$', views.callreports_create, name='callreports_create'),
    
    
]