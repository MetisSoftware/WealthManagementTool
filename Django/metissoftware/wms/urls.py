from django.conf.urls import patterns, url

from wms import views

urlpatterns = patterns('wms.views',
    url(r'^$', 'index', name='index'),
    url(r'^clients/', 'print_client', name='print_client'),
    )