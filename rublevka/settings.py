# -*- coding: utf-8 -*-

import os.path
import os

# Тут хранится корневая папка проекта как юникод-строка. Важно юникод. Чтоб не было проблем с русскими буквами.
PROJECT_DIR = os.path.join(os.path.dirname(unicode(__file__)), "..")

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Павел Войтко', 'pvoytko@gmail.com'),
)

MANAGERS = ADMINS


# Флаг что это локальный сайт Павла (надо для особых там БД-настроек)
IS_VOYTKO_COMP = os.path.dirname(os.path.abspath(__file__)) == "C:\\Users\\User\\Documents\\GitHub\\rublevka\\rublevka"
IS_VOYTKO_COMP = IS_VOYTKO_COMP or (os.path.dirname(os.path.abspath(__file__)) == "D:\\GitRepos\\rublevka\\rublevka")


# Медию загружаем из общей папки для всех серверных инстансов
JQ_MEDIA_FROM_RUBLEVKA_COM = not IS_VOYTKO_COMP


# В зависимости от условия выбирает либо одно либо другое значение.
# удобно использовать при конфигурации БД в зависимости от сайта (разработческий, боевой, ...)
def selectConfig(cond, valTrue, valFalse):
    return valTrue if cond else valFalse


# Конфиг БД для всех инстансов сайта
DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.mysql',
        'NAME':     'rublevka',
        'USER':     selectConfig(IS_VOYTKO_COMP, 'root',         'rublevka'),
        'PASSWORD': selectConfig(IS_VOYTKO_COMP, 'mysql',        'fNWl2zyB'),
        'HOST':     selectConfig(IS_VOYTKO_COMP, '127.0.0.1',    'localhost'),
    },
}


# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Moscow'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'ru'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Медию для всех серверных инстансов сайтов  грузим из /var/www/rublevka.com/media
# (это общее место хранения медии для всех серверных инстансов сайта).
if JQ_MEDIA_FROM_RUBLEVKA_COM:
    MEDIA_ROOT = os.path.join(PROJECT_DIR, '/var/www/rublevka.com/media')
else:
    MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
# STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')

# Additional locations of static files
STATICFILES_DIRS = [
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    # os.path.join(PROJECT_DIR, 'static'),
]

# Во время отладки - настраиваем джангу чтобы она подгружала статику из папки /static
# но не выставляла папку для collect, а на реальном сервере - выставляем папку для коллект но джанга не подгружает
# статику. На одной машине и коллект задать и подгрузку для джанги из одной паки низя - джанга на это ругается.
if IS_VOYTKO_COMP:
    STATICFILES_DIRS.append(os.path.join(PROJECT_DIR, 'static'))
else:
    STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')


# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'r+o_m_$#l9=eo&l$hvmnm+s$#9@omnh!8aiuv)qgxox1s=e^q7'

INSTAGRAM_CLIENT_ID = os.environ['INSTAGRAM_CLIENT_ID']
INSTAGRAM_CLIENT_SECRET = os.environ['INSTAGRAM_CLIENT_SECRET']
INSTAGRAM_ACCESS_TOKEN = os.environ['INSTAGRAM_ACCESS_TOKEN']

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    'django.core.context_processors.request',
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "rublevka.models.mainMenuContextProcessor"
)

ROOT_URLCONF = 'rublevka.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'rublevka.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_DIR, 'rublevka/templates/')
)

INSTALLED_APPS = (
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'south',
    'tinymce',
    'rublevka',
    'sorl.thumbnail',  # при первом обращении к картинке нарезает превьюшку для нее по указанным в теге размерам
)

ADMIN_TOOLS_INDEX_DASHBOARD = 'rublevka.dashboard.CustomIndexDashboard'

# Количество статей/новостей/блогов на странице
OBJECTS_PER_PAGE = 30


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

TINYMCE_JS_URL = '/static/libs/tinymce/js/tinymce/tinymce.min.js'
TINYMCE_JS_ROOT = os.path.join(PROJECT_DIR, 'static/libs/tinymce/js/tinymce')
TINYMCE_DEFAULT_CONFIG = {
    'theme_advanced_buttons3_add': 'code',
}
