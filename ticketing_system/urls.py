from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^tickets/$', 'tickets.views.index'),
    url(r'^tickets/user/1/(?P<ticket_id>\d+)/$', 'users.views.normal'),
    url(r'^tickets/user/2/(?P<ticket_id>\d+)/$', 'users.view.manager'),
)
