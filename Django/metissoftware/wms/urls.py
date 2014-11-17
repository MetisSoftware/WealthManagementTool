from django.conf.urls import patterns, url
from wms.views import ClientCreate, ClientUpdate, ClientDelete

from wms import views

urlpatterns = patterns('wms.views',
    url(r'^$', 'index', name='index'),
    url(r'^clients/', 'print_client', name='print_client'),
    url(r'^new_client.html', 'new_client', name='new_client'),
    )
