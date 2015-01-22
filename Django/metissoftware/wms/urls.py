from django.conf.urls import patterns, url
from wms.views import ClientCreate, ClientUpdate, ClientDelete

from wms import views

urlpatterns = patterns('wms.views',
    # url(r'^$', 'new_client', name='new_client'),
    # url(r'^clients/', 'print_clients', name='print_clients'),
    )
