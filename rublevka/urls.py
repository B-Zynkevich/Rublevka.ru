# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',

     # Главная
     url(r'^$', 'rublevka.views.main', name='main'),
     url(r'^choose_sex/(?P<sex>[012])/$', 'rublevka.views.choose_sex', name='choose_sex'),

     # Страница отображения статей внутренняя
     url(r'^article/(?P<id>\d+)/$', 'rublevka.views.article', name='article'),
     # Фильтр по подрубрике и рубрике и полу
     url(r'^articles/r/(?P<filterByRubricId>\d+|a)/sr/(?P<filterBySubRubricId>\d+|a)/$', 'rublevka.views.article_list', name='rubric'),
     url(r'^articles/$', 'rublevka.views.article_list', name='articles'),


     url(r'^blog/(?P<id>\d+)/$', 'rublevka.views.blog_post', name='blog_post'),
     url(r'^blogs/$', 'rublevka.views.blog_post_list', name='blog_post_list'),
     url(r'^news/(?P<id>\d+)/$', 'rublevka.views.news', name='external_news'),
     url(r'^news/$', 'rublevka.views.news_list', name='external_news_list'),

     url(r'^life/$', 'rublevka.views.life', name='life'),

     # Админка редактирование статей
     url(r'^rublevka-admin/', include(admin.site.urls)),
     url(r'^tinymce/', include('tinymce.urls')),
     url(r'^jqfu_upload_ajax/', 'rublevka.views.jqfu_article_content_photo_upload_ajax'),

     url(r'^links/', 'rublevka.views.links'),

     url(r'^admin_tools/', include('admin_tools.urls')),

)

# Статик-файлы и медиа-файлы для дебаг-сервера
if settings.DEBUG:
    import os
    urlpatterns += patterns('',
        url(r'^media/(.*)$', 'django.views.static.serve', {'document_root': os.path.join(os.path.abspath(os.path.dirname(__file__)), '../media')}),
    )
