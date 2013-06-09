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
from appengine import GaeTestCase
from textn.views import TextView
from textn.models import Text
import json
import time


class TextViewTest(GaeTestCase):
    def setUp(self):
        GaeTestCase.setUp(self)
        self.text_view = TextView()

    def test_get(self):
        email = 'textn@example.com'
        self.login(email)
        text = Text(text='text', approvals=[])
        text.put()
        key = text.key.urlsafe()

        result = self.text_view.get(None, None)
        self.assertEqual(result.status_code, 200)
        self.assertDictEqual(json.loads(result.content), {'user': email})

        result = self.text_view.get(None, key + 'does_not_exist')
        self.assertEqual(result.status_code, 400)
        self.assertEqual(result.content, '')

        result = self.text_view.get(None, key)
        self.assertEqual(result.status_code, 200)
        self.assertDictEqual(json.loads(result.content), {
            'key': key,
            'user': email,
            'text': 'text',
            'updated_at': int(time.mktime(text.updated_at.timetuple())),
            'has_password': False,
            'approvals': []
        })

        self.logout()
        result = self.text_view.get(None, None)
        self.assertEqual(result.status_code, 401)
        self.assertEqual(result.content, '')

        result = self.text_view.get(None, key + 'does_not_exist')
        self.assertEqual(result.status_code, 400)
        self.assertEqual(result.content, '')
