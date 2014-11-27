from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('wms.views',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'new_client', name='new_client'),
    url(r'^clients/', 'print_client', name='print_client'),
)
