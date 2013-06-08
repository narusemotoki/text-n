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
import unittest
from textn.views import BaseView
from textn.models import Text
import os


class BaseViewTest(unittest.TestCase):
    def setUp(self):
        self.base_view = BaseView()

    def test_is_public(self):
        def is_public(password, approvals):
            text = Text(password=password, approvals=approvals)
            return self.base_view._is_public(text)

        self.assertTrue(is_public('', []))
        self.assertFalse(is_public('password', []))
        self.assertFalse(is_public('', ['example.com']))

    def test_to_login(self):
        self.assertEqual(
            self.base_view._to_login('%2F')._headers['location'],
            ('Location', '/auth/login/%2F')
        )

        encoded_url = 'https%3A%2F%2Ftext-n.appspot.com%2F'
        location = self.base_view._to_login(encoded_url)._headers['location']
        self.assertEqual(location, ('Location', '/auth/login/' + encoded_url))

    def test_get_current_user_email(self):
        self.assertIsNone(self.base_view._get_current_user_email())

        email = 'test@example.com'
        os.environ['USER_EMAIL'] = email
        self.assertEqual(self.base_view._get_current_user_email(), email)
