# -*- coding: utf-8 -*-
from google.appengine.ext import ndb


class Text(ndb.Model):
    user = ndb.UserProperty(auto_current_user_add=True, indexed=False)
    approvals = ndb.TextProperty(repeated=True)
    text = ndb.TextProperty(required=True)
    password = ndb.TextProperty()
    created_at = ndb.DateTimeProperty(auto_now_add=True, indexed=False)
    updated_at = ndb.DateTimeProperty(auto_now=True, indexed=False)
