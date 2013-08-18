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
from google.appengine.ext import ndb


class Text(ndb.Model):
    user = ndb.UserProperty(auto_current_user_add=True)
    approvals = ndb.TextProperty(repeated=True)
    text = ndb.TextProperty(required=True)
    password = ndb.TextProperty()
    created_at = ndb.DateTimeProperty(auto_now_add=True, indexed=False)
    updated_at = ndb.DateTimeProperty(auto_now=True, indexed=True)
