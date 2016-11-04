from django.conf.urls import url
import views

urlpatterns = [
    # list
    url(r'^list/$', views.list ,name='list'),
]