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
import os
import sys
sys.path.extend(
    [
        os.sep.join([os.getcwd(), 'appengine']),
        os.sep.join([os.getcwd(), 'google_appengine']),
        os.sep.join([os.getcwd(), 'google_appengine', 'lib', 'yaml', 'lib']),
        os.sep.join([os.getcwd(), 'google_appengine', 'lib', 'django-1.4']),
    ]
)
try:
    import google
    import pkgutil
    google.__path__ = pkgutil.extend_path(google.__path__, google.__name__)
except:
    pass

from google.appengine.api import (
    apiproxy_stub_map,
    datastore_file_stub,
    mail_stub,
    user_service_stub,
)

apiproxy_stub_map.apiproxy.RegisterStub(
    'user',
    user_service_stub.UserServiceStub()
)

apiproxy_stub_map.apiproxy.RegisterStub(
    'datastore_v3',
    datastore_file_stub.DatastoreFileStub(
        'ghostnet_tests',
        '/tmp/test.db',
        '/tmp/test.hist'
    )
)
apiproxy_stub_map.apiproxy.RegisterStub(
    'mail',
    mail_stub.MailServiceStub()
)

os.environ['DJANGO_SETTINGS_MODULE'] = 'textn.settings'
from google.appengine.api import memcache
sys.modules['memcache'] = memcache

import unittest
from google.appengine.ext import testbed


class GaeTestCase(unittest.TestCase):
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

    def tearDown(self):
        self.logout()
        self.testbed.deactivate()

    def login(self, email):
        os.environ['USER_EMAIL'] = email

    def logout(self):
        del os.environ['USER_EMAIL']
