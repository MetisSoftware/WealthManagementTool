from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout

urlpatterns = patterns('wms.views',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'index', name='index'),
    url(r'^new_client.html', 'new_client', name='new_client'),
    url(r'^clients/', 'print_clients', name='print_clients'),
    url(r'^client_details/', 'client_details', name='client_details'),
    url(r'^wms/login/$', login, {'template_name': 'wms/login.html'}),
    url(r'^wms/logout/$', logout, {'next_page': '/'}),
    url(r'^appointments/', 'appointments', name='appointments'),
)
