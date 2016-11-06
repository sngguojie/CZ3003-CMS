from django.conf.urls import url
import views

urlpatterns = [
    # create
    url(r'^create/$', views.create ,name='create'),
    #create_for_first_time_active
    url(r'^create_for_first_time_active/$', views.create_for_first_time_active ,name='create_for_first_time_active'),
]