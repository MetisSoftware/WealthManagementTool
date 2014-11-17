from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('wms.views',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'index', name='index'),
    url(r'^clients/', 'print_client', name='print_client'),
    url(r'^create_client/', 'create_client', name='create_client'),


)
