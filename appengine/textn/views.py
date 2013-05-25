# -*- coding: utf-8 -*-
from google.appengine.api import users
from models import Text
from google.appengine.ext.ndb import Key
import json
from django.http import HttpResponse
from django.views.generic import View
import time


class TextView(View):
    def _render_to_json_response(self, source):
        return HttpResponse(json.dumps(source), mimetype='application/json')

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
                return HttpResponse(status=404)
        else:
            json_source = {
                'user': users.get_current_user().email()
            }
        return self._render_to_json_response(json_source)

    def post(self, request, key):
        data = json.loads(request.raw_post_data)
        text = Text(
            text=data['text'],
            approvals=data['approvals']
        )
        if 'password' in data:
            # TODO: hash
            text.password = data['password']

        return self._render_to_json_response({'key': text.put().urlsafe()})


class PlaneTextView(View):
    def get(self, request, key):
        return HttpResponse(Key(urlsafe=key).get().text, mimetype='text/plain')
