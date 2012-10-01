from django.conf.urls.defaults import patterns, include, url
from activityApp.views import *

urlpatterns = patterns('',
    url(r'^count/hourly/', CountHourlyView.link_to_view, name='count-hourly'),
)
