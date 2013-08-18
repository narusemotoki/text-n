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
from textn.views import MineView
from textn.models import Text
import json
import datetime


class MineViewTest(GaeTestCase):
    EMAIL = 'textn@example.com'

    def setUp(self):
        GaeTestCase.setUp(self)
        self.mine_view = MineView()
        self.login(MineViewTest.EMAIL)
        text1 = Text(text='text1', approvals=[])
        text1.updated_at = datetime.datetime(2013, 1, 1, 0, 0, 0, 0)
        text1.put()
        Text(text='text2', approvals=[]).put()

        self.login('other' + MineViewTest.EMAIL)
        Text(text='text3', approvals=[]).put()

    def test_get(self):
        self.login(MineViewTest.EMAIL)

        result = self.mine_view.get(None)
        self.assertEqual(result.status_code, 200)
        content = json.loads(result.content)
        self.assertEqual(len(content), 2)
        self.assertEqual(content[0]['text'], 'text2')
        self.assertEqual(content[1]['text'], 'text1')

        self.logout()
        result = self.mine_view.get(None)
        self.assertEqual(result.status_code, 200)
        content = json.loads(result.content)
        self.assertEqual(len(content), 0)
