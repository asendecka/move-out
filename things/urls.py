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
]
