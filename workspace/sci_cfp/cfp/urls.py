from django.conf.urls import url

from cfp import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'login', views.login_user, name='login'),
    url(r'signup', views.signup_user, name='signup'),
    url(r'search', views.search, name='search'),
    url(r'logout', views.logout_user, name='logout'),
    url(r'^event/([a-zA-Z0-9 ]+)/$', views.event, name='events'),
]