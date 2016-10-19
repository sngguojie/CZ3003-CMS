from django.conf.urls import url
import views
import views_deprec

urlpatterns = [
    # Deprecated, remove after client has been updated
    url(r'^create/$', views_deprec.create ,name='create'),
]