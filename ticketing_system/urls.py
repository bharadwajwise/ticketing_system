from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^tickets/$', 'tickets.views.index'),
    url(r'^tickets/(?P<ticket_id>\d+)/$', 'tickets.views.detail'),
    url(r'^tickets/add/$', 'tickets.views.add_ticket'),
)
