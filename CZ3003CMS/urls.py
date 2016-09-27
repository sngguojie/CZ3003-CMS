from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()
import settings
import hello.views

# Examples:
# url(r'^$', 'CZ3003CMS.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', hello.views.index, name='index'),
    url(r'^db', hello.views.db, name='db'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^Incident/', include('Incident.urls', namespace='Incident')),
    url(r'^IncidentSummary/', include('IncidentSummary.urls', namespace='IncidentSummary')),
]

