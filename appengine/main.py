import os
import sys
import django.core.handlers.wsgi
from google.appengine.api import memcache

sys.modules['memcache'] = memcache
os.environ['DJANGO_SETTINGS_MODULE'] = 'textn.settings'

app = django.core.handlers.wsgi.WSGIHandler()
