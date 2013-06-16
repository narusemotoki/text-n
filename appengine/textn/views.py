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
from django.http import (
    HttpResponse,
    HttpResponseForbidden,
    HttpResponseNotFound,
    HttpResponseBadRequest,
)
from django.views.generic import View
import time
from django.shortcuts import redirect
import urllib
from django.core.urlresolvers import reverse
from PIL import Image, ImageDraw, ImageFont
import string


def login(request, redirect_to):
    dest_url = urllib.unquote_plus(redirect_to) if redirect_to else '/'
    print dest_url

    return redirect(users.create_login_url(dest_url))


def logout(request):
    response = redirect('/')
    response.delete_cookie('dev_appserver_login')
    response.delete_cookie('SACSID')
    response.delete_cookie('ACSID')

    return response


class HttpResponseUnauthorized(HttpResponse):
    status_code = 401


class BaseView(View):
    def _get_cache_or_datastore(self, urlsafe_key):
        return Key(urlsafe=urlsafe_key).get()

    def _text2dict(self, text):
        return {
            'key': text.key.urlsafe(),
            'user': text.user.email(),
            'text': text.text,
            'approvals': text.approvals,
            'updated_at': int(time.mktime(text.updated_at.timetuple())),
            'has_password': True if text.password else False
        }

    def _get_current_user_email(self):
        user = users.get_current_user()
        if user:
            return user.email()

        return None

    def _render_to_json_response(self, source):
        return HttpResponse(json.dumps(source), mimetype='application/json')

    def _has_read_permission(self, text):
        if self._is_owner(text):
            return True

        if self._has_allowed(text):
            return True

        return False

    def _is_public(self, text):
        return not text.password and len(text.approvals) == 0

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

    def _to_login(self, dest_url):
        return redirect(reverse('textn.views.login', args=[dest_url]))


class TextView(BaseView):
    def get(self, request, key):
        if key:
            try:
                text = Key(urlsafe=key).get()
                if not text.password and self._has_read_permission(text):
                    return self._render_to_json_response(self._text2dict(text))
                elif not self._is_public(text):
                    return HttpResponseUnauthorized()
            except:
                return HttpResponseBadRequest()

        email = self._get_current_user_email()
        if not email:
            return HttpResponseUnauthorized()
        return self._render_to_json_response({'user': email})

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

        return self._render_to_json_response(self._text2dict(text))


class PlaneTextView(BaseView):
    def _render_to_plane_text_response(self, plane_text):
        return HttpResponse(plane_text, mimetype='text/plain; charset="utf-8"')

    def get(self, request, key):
        text = Key(urlsafe=key).get()
        if not text:
            return HttpResponseNotFound()

        if not text.password and self._has_read_permission(text):
            return self._render_to_plane_text_response(text.text)
        elif not self._is_public(text):
            return self._to_login(urllib.quote_plus('plaintext/' + key))
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

        if not text.password and self._has_read_permission(text):
            return self._render_to_plane_text_response(text.text)
        return HttpResponseForbidden()


class ImageTextView(BaseView):
    def _render_image(self, text):
        image = Image.new('RGB', (1024, 1024), 'black')
        draw = ImageDraw.Draw(image)
        font_path = 'fonts/VL-Gothic-Regular.ttf'
        font = ImageFont.truetype(font_path, 15, encoding='utf-8')

        width = 0
        height = 0
        for line in text.text.splitlines():
            formatted = string.expandtabs(line, 8)
            textsize = draw.textsize(formatted, font)
            draw.text((0, height), formatted, font=font, fill='white')
            width = max(textsize[0], width)
            height += textsize[1]

        response = HttpResponse(mimetype='image/png')
        image.crop((0, 0, width, height)).save(response, 'PNG')

        return response

    def get(self, request, key):
        text = Key(urlsafe=key).get()
        if not text:
            return HttpResponseNotFound()

        if not text.password and self._has_read_permission(text):
            return self._render_image(text)
        return HttpResponseForbidden()
