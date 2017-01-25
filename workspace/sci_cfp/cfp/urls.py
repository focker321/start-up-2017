from django.conf.urls import url

from cfp import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]