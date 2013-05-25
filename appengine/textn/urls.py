# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns
from views import TextView, PlaneTextView


urlpatterns = patterns(
    '',
    (r'^api/text/?(?P<key>.*)$', TextView.as_view()),
    (r'^planetext/?(?P<key>.*)$', PlaneTextView.as_view())
)
