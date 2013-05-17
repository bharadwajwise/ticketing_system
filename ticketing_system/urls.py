from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^tickets/$', 'tickets.views.index'),
    url(r'^tickets/(?P<ticket_id>\d+)/$', 'tickets.views.detail'),
    url(r'^tickets/add/$', 'tickets.views.add_ticket'),
    url(r'^user/(?P<user_id>\S+)/$', 'tickets.views.view_ticket'), 
    url(r'^admin/', include(admin.site.urls)),
    url(r'^create/(?P<user_id>\S+)/$', 'tickets.views.add_ticket'),
    url(r'^login/', 'tickets.views.loginview'),
    url(r'^auth/', 'tickets.views.auth_and_login'),
    url(r'^signup/', 'tickets.views.sign_up'),
)