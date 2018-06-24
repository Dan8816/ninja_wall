from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^create$', views.create),
    url(r'^confirm$', views.confirm),
    url(r'^success$', views.success),
    url(r'^success/post_msg$', views.create_msg),
    url(r'^(?P<id>\d+)/del_msg$', views.del_msg),
    url(r'^(?P<id>\d+)/like$', views.like),
    url(r'^post_cmnt$', views.create_cmnt),
    url(r'^(?P<id>\d+)/del_comnt$', views.del_comnt),
     url(r'^success/populars$', views.populars),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
]