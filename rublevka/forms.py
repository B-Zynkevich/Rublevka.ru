#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Evgeniy Pokidov
# @Date:   2013-11-05 21:42:08
# @Email:  pokidovea@gmail.com
# @Last modified by:   pokidovea
# @Last Modified time: 2013-12-04 11:22:14

from django import forms
from models import Article
from tinymce.widgets import TinyMCE
from django.conf import settings
import os


# Виджет для header меняем на однострочный (вместо большого многострочного)
# И видежт для контента делаем на основе tiny mce.
class ArticleAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ArticleAdminForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        m = super(ArticleAdminForm, self).save(commit=False)

        # Принимает объект InMemoryUploadedFile
        # Из него грузит объект картинку.
        # Измеяет ее пропорционально так чтобы ширина стала newWidth
        # Создает новый InMemoryUploadedFile с картинкой и возвращает его.
        def resizeByWidth(inMemFile, newWidth, fName=None):
            inMemFile.seek(0)
            # Приводим изображение к ширине
            from PIL import Image
            im = Image.open(inMemFile)
            ratio = newWidth / float(im.size[0])
            im = im.resize((newWidth, int(im.size[1]*ratio)), Image.ANTIALIAS)

            # Сохраняем его обратно в файл
            from django.core.files.uploadedfile import InMemoryUploadedFile
            import StringIO
            im_io = StringIO.StringIO()
            im.save(im_io, inMemFile.content_type.split("/")[1])
            fileObj = InMemoryUploadedFile(im_io, None, fName if fName else inMemFile.name, inMemFile.content_type, im_io.len, None)
            fileObj.seek(0)
            return fileObj

        # Если при редактировании модели было задано поле фото, то
        if m.photo._file:

            # Выполняем 2 задачи.
            # 1. Приводим изображение из модели к ширине 606 (такой размер имеет фотка на главной)
            # 2. Сохраняем его обратно в модель
            flObj = resizeByWidth(m.photo._file, Article.PHOTO_WIDTH)
            m.photo._file = flObj

            # 2. Цепляем к save сохранение превью с изображением с шириной 293
            oldSave = m.save

            def saveWithPreview():

                # Сначала дефолтово сохранение для модели (сохранит основной файл с изображением)
                from django.core.files.storage import default_storage
                from django.core.files.base import ContentFile
                oldSave()

                # Сейчас сохранение превьюшки
                previewFilePath = os.path.join(settings.MEDIA_ROOT, m.small_photo)
                fName = os.path.basename(m.photo.name)
                flObj2 = resizeByWidth(flObj, Article.SMALL_PHOTO_WIDTH, fName)
                default_storage.save(previewFilePath, ContentFile(flObj2.read()))
            m.save = saveWithPreview

        # Сохраняем если надо
        if commit:
            m.save()

        return m

    # A template for a very customized change view:
    class Meta:
        model = Article
        widgets = {
            'header': forms.TextInput(attrs={'size': 112}),
            'content': TinyMCE(attrs={'rows': 30}, mce_attrs={
                'theme': 'modern',
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
            }),
            'short_descr': forms.Textarea(attrs={'cols': 80, 'rows': 4}),
        }
