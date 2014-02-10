#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Evgeniy Pokidov
# @Date:   2013-11-05 20:07:23
# @Email:  pokidovea@gmail.com
# @Last modified by:   pokidovea
# @Last Modified time: 2013-12-05 12:55:53

from settings import *


# Конфиг БД для всех инстансов сайта
DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.mysql',
        'NAME':     'rublevka',
        'USER':     'root',
        'PASSWORD': 'zqecsawdx',
        'HOST':     'localhost',
        'TEST_CHARSET': 'utf8',
    },
}

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media')

MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

INSTALLED_APPS += (
    'debug_toolbar',
    'django_any'
)

USE_TZ = False
SOUTH_TESTS_MIGRATE = False  # При тестировании будет использоваться syncdb вместо migrate

DEBUG_TOOLBAR_PANELS = (
    # 'debug_toolbar.panels.version.VersionDebugPanel', # убрать. только место занимает.
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.cache.CacheDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
)
DEBUG_TOOLBAR_CONFIG = {
    'EXCLUDE_URLS': ('/rublevka-admin',),
    'INTERCEPT_REDIRECTS': False,
}
INTERNAL_IPS = ('127.0.0.1',)
