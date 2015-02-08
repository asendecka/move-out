from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.thing_list, name='list'),
    url(r'^detail/(?P<pk>[0-9]+)/$', views.thing_detail, name='detail'),
    url(r'^take/(?P<pk>[0-9]+)/$', views.thing_take, name='take'),
    url(r'^back/(?P<pk>[0-9]+)/$', views.thing_give_back, name='give_back'),
    url(r'^add/$', views.thing_add, name='add'),
    url(r'^taker/send/(?P<taker_pk>[0-9]+)/$', views.send_mail_to_taker,
        name='send_mail_to_taker'),
    url(r'^taker/list/$', views.taker_list, name='taker_list'),
    url(r'^taker/my_things/$', views.my_things, name='my_things'),
    url(r'^taker/taker_things/(?P<taker_pk>[0-9]+)/$', views.taker_things,
        name='taker_things'),
    url(r'^taker/gone/(?P<pk>[0-9]+)/$', views.thing_gone, name='thing_gone'),
    url(r'^taker/not_gone/(?P<pk>[0-9]+)/$', views.thing_not_gone,
        name='thing_not_gone'),
]
