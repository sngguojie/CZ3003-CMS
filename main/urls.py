from django.conf.urls import url
import views

urlpatterns = [
    url(r'^list_logs/(?P<incident_id>[0-9]+)/$', views.list_logs_for_incident ,name='list_logs'),
]