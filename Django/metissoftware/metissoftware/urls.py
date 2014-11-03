from django.conf.urls import patterns, include, url
from django.contrib import admin
from views import current_datetime

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'metissoftware.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^time/$', current_datetime),
)
