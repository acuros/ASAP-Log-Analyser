from django.conf.urls.defaults import patterns, include, url
from django.shortcuts import render
from activityApp.views import *

urlpatterns = patterns('',
    url(r'^count/hourly/', CountHourlyView.link_to_view, name='count-hourly'),
    url(r'^graph/day/', lambda request:render(request, 'date_graph.html'))
)
