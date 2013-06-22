# -*- coding: utf-8 -*-
"""
text-n
Copyright (C) 2013 Motoki Naruse <motoki@naru.se>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from django.conf.urls import patterns
from views import TextView, PlaneTextView, ImageTextView, MineView


urlpatterns = patterns(
    'textn.views',
    (r'^api/text/?(?P<key>.*)$', TextView.as_view()),
    (r'^api/imagetext/?(?P<key>.*)\.png$', ImageTextView.as_view()),
    (r'^api/mine$', MineView.as_view()),
    (r'^plaintext/?(?P<key>.*)$', PlaneTextView.as_view()),
    (r'^auth/login/(?P<redirect_to>.*)$', 'login'),
    (r'^auth/logout$', 'logout'),
)
