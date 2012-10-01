from django.conf.urls.defaults import patterns, include, url
from meeting.views import *

urlpatterns = patterns('',
     url(r'^list/', MeetingListView.link_to_view),
     url(r'^university-list/', UniversityListView.link_to_view),
     url(r'^add/', MeetingAddView.link_to_view),
     url(r'^comment/list/', CommentListView.link_to_view),
     url(r'^comment/add/', CommentAddView.link_to_view),
     url(r'^plus/', PlusView.link_to_view),
)
