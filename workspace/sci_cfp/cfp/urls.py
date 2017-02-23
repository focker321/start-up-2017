from django.conf.urls import url

from cfp import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'login', views.login_user, name='login'),
    url(r'signup', views.signup_user, name='signup'),
    url(r'profile', views.profile, name='profile'),
    url(r'search', views.search, name='search'),
    url(r'logout', views.logout_user, name='logout'),
    url(r'favorite', views.favorite, name='favorite'),
    url(r'getcategories', views.get_categories, name='get_categories'),
    url(r'notification/active', views.notification_active, name='notification_active'),
    url(r'event/review/new', views.event_review, name='event_review'),
    url(r'event/review', views.review, name='review'),
    url(r'^event/([a-zA-Z0-9 _-]+)/$', views.event, name='events'),
]