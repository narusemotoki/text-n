# -*- coding: utf-8 -*-
from google.appengine.api import users
from models import Text
from google.appengine.ext.ndb import Key
import json
from django.http import HttpResponse, HttpResponseForbidden
from django.http import HttpResponseNotFound, HttpResponseBadRequest
from django.views.generic import View
import time


class HttpResponseUnauthorized(HttpResponse):
    status_code = 401


class BaseView(View):
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

        if len(text.approvals) == 0:
            return True
        email = self._get_current_user_email()
        if not email:
            return False

        for approval in text.approvals:
            if '@' in approval:
                if email == approval:
                    break
            elif email.endswith('@' + approval):
                break
        else:
            return False

    def _is_owner(self, text):
        return text.user.email() == self._get_current_user_email()


class TextView(BaseView):
    def get(self, request, key):
        if key:
            text = Key(urlsafe=key).get()
            if text:
                json_source = {
                    'user': text.user.email(),
                    'text': text.text,
                    'approvals': text.approvals,
                    'updated_at': time.mktime(text.updated_at.timetuple())
                }
            else:
                return HttpResponseNotFound()
        else:
            email = self._get_current_user_email()
            if not email:
                return HttpResponseUnauthorized()
            json_source = {
                'user': email
            }
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

        return self._render_to_json_response({'key': text.put().urlsafe()})


class PlaneTextView(BaseView):
    def _render_to_plane_text_response(self, plane_text):
        return HttpResponse(plane_text, mimetype='text/plain')

    def get(self, request, key):
        text = Key(urlsafe=key).get()
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
