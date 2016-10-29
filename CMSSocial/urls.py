from django.conf.urls import url
import views

urlpatterns = [
    # update
    url(r'^update/$', views.update ,name='update'),
]