import os
import sys

sys.path.append('/var/www/bogdan.rublevka.com')
os.environ['DJANGO_SETTINGS_MODULE'] = 'rublevka.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()