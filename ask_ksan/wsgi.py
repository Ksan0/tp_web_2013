import os, sys

# sys.path.append('/usr/local/lib/python2.7/dist-packages/django/')

# sys.path.append('/home/ksan/TP/Web/Project/ask_ksan/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'ask_ksan.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()