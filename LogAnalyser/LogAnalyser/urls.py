from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
#from django.contrib import admin
#admin.autodiscover()

import os

static = os.path.join(settings.PROJECT_PATH, 'static')

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'oic.views.home', name='home'),
    url(r'^meeting/', include('meeting.urls')),
    url(r'^activity/', include('activityApp.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    #url(r'^admin/', include(admin.site.urls)),

    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', { 'document_root':static}),
)
