from django.conf.urls.defaults import patterns, include, url
#from django.contrib import admin
#admin.autodiscover()

import os, settings

css = os.path.join(os.path.dirname(os.path.dirname(__file__)),'static/css')
img = os.path.join(os.path.dirname(os.path.dirname(__file__)),'static/img')
js = os.path.join(os.path.dirname(os.path.dirname(__file__)),'static/js')

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'oic.views.home', name='home'),
    url(r'^meeting/', include('meeting.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    #url(r'^admin/', include(admin.site.urls)),

    url(r'^static/css/(?P<path>.*)$', 'django.views.static.serve', { 'document_root':css}),
    url(r'^static/js/(?P<path>.*)$', 'django.views.static.serve', { 'document_root':js}),
    url(r'^static/img/(?P<path>.*)$', 'django.views.static.serve', { 'document_root':img}),
)
