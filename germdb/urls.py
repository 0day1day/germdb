from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'germdb.views.home', name='home'),
    url(r'^collector/', include('collector.urls')),
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)
