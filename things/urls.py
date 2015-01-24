from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.thing_list, name='list'),
    url(r'^detail/(?P<pk>[0-9]+)/$', views.thing_detail, name='detail'),
    url(r'^take/(?P<pk>[0-9]+)/$', views.thing_take, name='take'),
    url(r'^back/(?P<pk>[0-9]+)/$', views.thing_give_back, name='give_back'),
]
