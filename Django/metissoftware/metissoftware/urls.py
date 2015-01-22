from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import login

urlpatterns = patterns('wms.views',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'index', name='index'),
    url(r'^new_client.html', 'new_client', name='new_client'),
    url(r'^clients/', 'print_client', name='print_client'),
    url(r'^wms/login/$', login, {'template_name': 'wms/login.html'}),
    url(r'^appointments/', 'appointments', name='appointments'),
)
