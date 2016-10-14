from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()
import settings
import main.views

# Examples:
# url(r'^$', 'CZ3003CMS.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', main.views.index, name='index'),
    url(r'^db', main.views.db, name='db'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^main/', include('main.urls', namespace='main')),
    url(r'^Incident/', include('Incident.urls', namespace='Incident')),
    url(r'^IncidentSummary/', include('IncidentSummary.urls', namespace='IncidentSummary')),
    url(r'^IncidentLocation/', include('IncidentLocation.urls', namespace='IncidentLocation')),
    url(r'^IncidentLog/', include('IncidentLog.urls', namespace='IncidentLog')),
    url(r'^Agency/', include('Agency.urls', namespace='Agency')),
    url(r'^SMS/', include('SMS.urls', namespace='SMS')),
    url(r'^IncidentCallReport/', include('IncidentCallReport.urls', namespace='IncidentCallReport')),

]

