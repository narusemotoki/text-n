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
from google.appengine.api import users
from models import Text
from google.appengine.ext.ndb import Key
import json
from django.http import HttpResponse, HttpResponseForbidden
from django.http import HttpResponseNotFound, HttpResponseBadRequest
from django.views.generic import View
import time
from django.core.cache import cache


class HttpResponseUnauthorized(HttpResponse):
    status_code = 401


class BaseView(View):
    def _setCache(self, text):
        cache.set(text.key.urlsafe(), text, 86400)

    def _getCacheOrDatastore(self, urlsafe_key):
        cached = cache.get(urlsafe_key)
        text = cached if cached else Key(urlsafe=urlsafe_key).get()
        if text:
            self._setCache(text)
        return text

    def _text2dict(self, text):
        d = {
            'key': text.key.urlsafe(),
            'user': text.user.email(),
            'text': text.text,
            'approvals': text.approvals,
            'updated_at': time.mktime(text.updated_at.timetuple())
        }
        d['has_password'] = True if text.password else False

        return d

    def _get_current_user_email(self):
        user = users.get_current_user()
        if user:
            return user.email()

        return None

    def _render_to_json_response(self, source):
        return HttpResponse(json.dumps(source), mimetype='application/json')

    def _has_read_permission(self, request, text):
        if self._is_owner(text):
            return True

        if self._has_allowed(text):
            return True

    def _has_allowed(self, text):
        if len(text.approvals) == 0:
            return True
        email = self._get_current_user_email()
        if not email:
            return False

        for approval in text.approvals:
            if '@' in approval:
                if email == approval:
                    return True
            elif email.endswith('@' + approval):
                return True
        return False

    def _is_owner(self, text):
        return text.user.email() == self._get_current_user_email()


class TextView(BaseView):
    def get(self, request, key):
        json_source = None
        if key:
            text = self._getCacheOrDatastore(key)
            if not text.password and self._has_read_permission(request, text):
                json_source = self._text2dict(text)

        if not json_source:
            email = self._get_current_user_email()
            if not email:
                return HttpResponseUnauthorized()
            json_source = {'user': email}
        return self._render_to_json_response(json_source)

    def post(self, request, key):
        data = json.loads(request.raw_post_data)
        text = Text(text=data['text'], approvals=[])

        if 'approvals' in data:
            for approval in data['approvals']:
                if approval:
                    text.approvals.append(approval)

        if 'password' in data:
            # TODO: hash
            text.password = data['password']
        text.put()
        self._setCache(text)

        return self._render_to_json_response(self._text2dict(text))


class PlaneTextView(BaseView):
    def _render_to_plane_text_response(self, plane_text):
        return HttpResponse(plane_text, mimetype='text/plain; charset="utf-8"')

    def get(self, request, key):
        text = self._getCacheOrDatastore(key)
        if not text:
            return HttpResponseNotFound()

        if not text.password and self._has_read_permission(request, text):
            return self._render_to_plane_text_response(text.text)

        return HttpResponseForbidden()

    def post(self, request, key):
        if not 'key' in request.POST:
            return HttpResponseBadRequest()

        text = Key(urlsafe=key).get()
        if not text:
            return HttpResponseNotFound()

        if text.password:
            if not 'password' in request.POST:
                return HttpResponseBadRequest()
            elif not text.password == request.POST['password']:
                return HttpResponseUnauthorized()

        if not text.password and self._has_read_permission(request, text):
            return self._render_to_plane_text_response(text.text)
        return HttpResponseForbidden()
