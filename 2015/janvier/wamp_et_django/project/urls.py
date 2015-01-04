from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^ping/', 'votreapp.views.ping'),
    url(r'^$', 'votreapp.views.index')
)
