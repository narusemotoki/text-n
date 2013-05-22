MIDDLEWARE_CLASSES = ('django.middleware.common.CommonMiddleware',)

INSTALLED_APPS = ('textn',)

ROOT_URLCONF = 'textn.urls'

import os
ROOT_PATH = os.path.dirname(__file__)
TEMPLATE_DIRS = (ROOT_PATH + '/templates',)

CACHE_BACKEND = 'memcached:///'
