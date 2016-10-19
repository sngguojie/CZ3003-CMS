from django.conf.urls import url
import views
import IncidentLog.views

urlpatterns = [
    # Deprecated, please delete when client has been updated
    url(r'^list_logs/(?P<incident_id>[0-9]+)/$', IncidentLog.views.get_logs_for_incident ,name='list_logs'),
]