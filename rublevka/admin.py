#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Evgeniy Pokidov
# @Date:   2013-11-05 21:36:37
# @Email:  pokidovea@gmail.com
# @Last modified by:   pokidovea
# @Last Modified time: 2013-12-04 11:22:43

from django.contrib import admin
from django.db import models as db_models
from tinymce.widgets import TinyMCE
from django.utils.safestring import mark_safe
from django.utils.html import escape
from django.conf.urls import patterns, url
from functools import update_wrapper
from django.shortcuts import render
import models
import forms

# Настройка формы для Article


# Возвращает callable объект который можно пердеавать в ModelAdmin.list_display
# имя заголовка в таблице будет columnCaption а в значении будет выводится поле objPropertyName модели.
def listDisplayField(objPropertyName, columnCaption):
    def wrapper(obj):
        return getattr(obj, objPropertyName)
    wrapper.short_description = columnCaption
    return wrapper


class ModelAdminWithPreview(admin.ModelAdmin):

    change_form_template = 'admin/change_form_with_preview.html'

    def __init__(self, *args, **kwargs):
        super(ModelAdminWithPreview, self).__init__(*args, **kwargs)

        if not hasattr(self, 'preview_template'):
            raise RuntimeError('Improperly configured')

    def get_urls(self):

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)

        urls = super(ModelAdminWithPreview, self).get_urls()

        info = self.model._meta.app_label, self.model._meta.module_name

        custom_urls = patterns('',
                               url(r'^(.+)/preview/$',
                                   wrap(self.preview),
                                   name="%s_%s_admin_preview" % info))

        return custom_urls + urls

    def preview(self, request, object_id):

        article_object = self.model.objects.get(id=object_id)
        return render(request, self.preview_template, {'article_object': article_object})


class ArticleAdmin(ModelAdminWithPreview):
    preview_template = 'article.html'
    list_display = ('header', 'is_important', )
    list_filter = ('is_important', )
    list_editable = ('is_important', )
    filter_horizontal = ('tags',)
    form = forms.ArticleAdminForm


# Настройка списка для Rubric
class RubricAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'in_more')
    list_editable = ('position', 'in_more',)


# Настройка списка для SubRubric
class SubRubricAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'position')


class BlogPostAdmin(ModelAdminWithPreview):
    preview_template = 'blog_post.html'
    list_display = ('title', 'author', 'date_publishing', 'for_sex', )
    list_filter = ('for_sex', )
    filter_horizontal = ('tags',)
    formfield_overrides = {
        db_models.TextField: {'widget': TinyMCE(attrs={'rows': 30},
                                                mce_attrs={'theme': 'modern',
                                                           'menubar': False,
                                                           'plugins': [
                                                           "autolink lists link imageupload anchor searchreplace media paste code"
                                                           ],
                                                           'toolbar_items_size': 'small',
                                                           'toolbar': "undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link imageupload code",

                                                           'style_formats': [
                                                               {'title': 'Заголовок', 'block': 'h1'},
                                                               {'title': 'Обычный текст', 'block': 'p'},
                                                           ],
                                                           'statusbar': False,
                                                           'width': 800
                                                           })},
    }


class ExternalNewsAdmin(ModelAdminWithPreview):
    preview_template = 'news.html'
    actions = ['make_published']
    list_display = ('title', 'clickable_link', 'clickable_media_content', 'date_publishing', 'for_sex', 'enabled',)
    list_filter = ('enabled', 'for_sex')
    list_editable = ('enabled',)
    readonly_fields = ('news_hash', 'date_publishing', 'clickable_full_link')
    search_fields = ('title', 'description', 'content', )
    fieldsets = (
        (None, {
            'fields': ('news_hash',
                       'title',
                       'clickable_full_link',
                       'enabled',
                       'for_sex',
                       'description',
                       'date_publishing',
                       'media_content',
                       'photo',
                       'content')
        }),
    )

    formfield_overrides = {
        db_models.TextField: {'widget': TinyMCE(attrs={'rows': 30},
                                                mce_attrs={'theme': 'modern',
                                                           'menubar': False,
                                                           'plugins': [
                                                           "autolink lists link imageupload anchor searchreplace media paste code"
                                                           ],
                                                           'toolbar_items_size': 'small',
                                                           'toolbar': "undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link imageupload code",

                                                           'style_formats': [
                                                               {'title': 'Заголовок', 'block': 'h1'},
                                                               {'title': 'Обычный текст', 'block': 'p'},
                                                           ],
                                                           'statusbar': False,
                                                           'width': 800
                                                           })},
    }

    def clickable_link(self, obj):
        """Делает из поля link короткую функционирующую ссылку"""

        return mark_safe(u'<a href="%(link)s">перейти</a>' % {'link': escape(obj.link)})
    clickable_link.short_description = u'Ссылка'

    def clickable_full_link(self, obj):
        """Делает из поля link длинную ссылку, с полным адресом"""

        return mark_safe(u'<a href="%(link)s">%(link)s</a>' % {'link': escape(obj.link)})
    clickable_full_link.short_description = u'Ссылка'

    def clickable_media_content(self, obj):
        """Делает из поля media_content ссылку"""

        if obj.media_content:
            return mark_safe(u'<a href="%(link)s">смотреть</a>' % {'link': escape(obj.media_content)})
        else:
            return u''
    clickable_media_content.short_description = u'Медиа контент'

    def make_published(self, request, queryset):
        queryset.update(enabled=True)
    make_published.short_description = u"Опубликовать выделенные новости"


class InstagramAccountAdmin(admin.ModelAdmin):
    list_display = ('instagram_id', 'profile_link', 'small_profile_picture', 'full_name')
    view_readonly_fields = ['profile_link', 'instagram_id', 'full_name', 'small_profile_picture']
    add_fieldsets = (
        (None, {'fields': ('username',)}),
    )
    view_fieldsets = (
        (None, {
            'fields': ('instagram_id',
                       'profile_link',
                       'small_profile_picture',
                       'full_name'
                       )
        }),
    )
    search_fields = ('username', 'full_name',)

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = []
        if obj is None:
            self.readonly_fields = []
            self.fieldsets = self.add_fieldsets
        else:
            self.fieldsets = self.view_fieldsets
            self.readonly_fields = self.view_readonly_fields

        return super(InstagramAccountAdmin, self).get_form(request, obj, **kwargs)

    def small_profile_picture(self, obj):
        return mark_safe(u'<img src="%(link)s" width="40px" height="40px">' % {'link': escape(obj.profile_picture)})
    small_profile_picture.short_description = u'Фото'

    def profile_link(self, obj):
        return mark_safe(u'<a href="%(link)s">%(username)s</a>' % {'link': escape(obj.profile_link), 'username': escape(obj.username)})
    profile_link.short_description = u'Имя пользователя'


class InstagramImageAdmin(admin.ModelAdmin):
    list_display = ('instagram_id', 'profile_link', 'small_picture', 'clickable_full_link', 'is_accepted')
    readonly_fields = ['instagram_id', 'profile_link', 'small_picture', 'big_picture', 'clickable_full_link']
    list_filter = ('is_accepted', 'account__username')
    list_editable = ('is_accepted',)
    ordering = ('-instagram_id', )
    fieldsets = (
        (None, {
            'fields': ('instagram_id',
                       'profile_link',
                       'clickable_full_link',
                       'big_picture',
                       'is_accepted'
                       )
        }),
    )

    def small_picture(self, obj):
        return mark_safe(u'<img src="%(link)s" width="40px" height="40px">' % {'link': escape(obj.url)})
    small_picture.short_description = u'Фото'

    def big_picture(self, obj):
        return mark_safe(u'<img src="%(link)s" width="300px" height="300px">' % {'link': escape(obj.url)})
    big_picture.short_description = u'Фото'

    def has_add_permission(self, request):
        return False

    def clickable_full_link(self, obj):
        """Делает из поля instagram_link длинную ссылку, с полным адресом"""

        return mark_safe(u'<a href="%(link)s">%(link)s</a>' % {'link': escape(obj.instagram_link)})
    clickable_full_link.short_description = u'Ссылка'

    def profile_link(self, obj):
        return mark_safe(u'<a href="%(link)s">%(full_name)s (%(username)s)</a>' % {'link': escape(obj.account.profile_link),
                                                                                   'full_name': escape(obj.account.full_name),
                                                                                   'username': escape(obj.account.username)})
    profile_link.short_description = u'Автор'


# Возможность редачить через админку
admin.site.register(models.Article, ArticleAdmin)
admin.site.register(models.Tag)
admin.site.register(models.Rubric, RubricAdmin)
admin.site.register(models.SubRubric, SubRubricAdmin)
admin.site.register(models.Author)
admin.site.register(models.BlogPost, BlogPostAdmin)
admin.site.register(models.ExternalNews, ExternalNewsAdmin)
admin.site.register(models.InstagramAccount, InstagramAccountAdmin)
admin.site.register(models.InstagramImage, InstagramImageAdmin)
