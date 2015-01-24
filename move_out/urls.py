from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'move_out.views.home', name='home'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^(?P<token>[\w, -]+)/', include('things.urls', namespace='things', app_name='things')),
)

if settings.DEBUG:
    urlpatterns += [
        url(r'^m/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    ]
