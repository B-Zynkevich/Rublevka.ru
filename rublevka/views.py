# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import simplejson
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from rublevka import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
import render_with_api
import os


def paginate_it(collection, page_num):
    """
    Разбивает коллекцию объектов на страницы.
    Возвращает объект паггинатора и объект текущей страницы.
    Подробнее о паггинации можно прочитать здесь https://docs.djangoproject.com/en/1.5/topics/pagination/
    """

    paginator = Paginator(collection, settings.OBJECTS_PER_PAGE)

    try:
        current_page = paginator.page(page_num)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        current_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        current_page = paginator.page(paginator.num_pages)

    return (paginator, current_page)

# Данный класс получает на вход список значений то как это надо для jQuery File Plugin
# и инициализирует ответ в формате JSON.


class JsonJQUFilesResponse(HttpResponse):

    """
    Returns an HTTP response with its data encoded in JSON format.
    """

    def __init__(self, request, data, *args, **kwargs):
        data = simplejson.dumps({'files': [data]})
        mime = "application/json" if "application/json" in request.META['HTTP_ACCEPT_ENCODING'] else 'text/plain'
        super(JsonJQUFilesResponse, self).__init__(data, mime, *args, **kwargs)


# Возвращает объект файл для сохранения фото статьи
# Полученное имя файла является основной для создания уникального имени в рамках папки.
def getAvaliableMediaContentPhotoFile(filename):
    fname = os.path.join(settings.MEDIA_ROOT, "article_content_photo", filename)
    from django.core.files.storage import FileSystemStorage
    fname = FileSystemStorage().get_available_name(fname)
    return open(fname, "wb+")


# Сохраняет файл, загруженный через плагин gjQuery Upload File, в папке на сервере.
# Вызывается либкой jQuery Upload File через Аякс.
@login_required
def jqfu_article_content_photo_upload_ajax(request):

    # Название папки внутри media в которой будут храниться загруженные в контент статьи файлы.
    ARTICLE_CONTENT_PHOTO_DIR_NAME = 'article_content_photo'

    # Сохраняем файл на диск
    memFile = request.FILES['file']
    diskFile = getAvaliableMediaContentPhotoFile(memFile.name)
    diskFile.write(memFile.read())

    # Возвращаем инфо о сохраненном файле - обратно в клиент.
    # Тут важно имя - memFile (как было у юзера на компе) а в УРЛ - diskFile (факт. имя на диске, может быть
    # другим, с суффиксом, если исходное имя уже занято).
    return JsonJQUFilesResponse(request, {
                                'name': memFile.name,
                                'url': settings.MEDIA_URL + ARTICLE_CONTENT_PHOTO_DIR_NAME + "/" + os.path.basename(diskFile.name),
                                })


# Главная, она же для всех фильтров
@render_with_api.render_with_api('main.html')
def main(request):

    # последние важные статьи
    important_articles = models.Article.objects.filter(is_important=True).order_by('-date_publishing')[:4]

    # Вылезла проблема с MySQL: база не поддерживает оператор IN O_o ... приходится костылить
    limits = [Q(object_id=i) for i in important_articles.values_list('id', flat=True)]
    content_type = ContentType.objects.get_for_model(models.Article)

    tape_object_list = models.MainTape.objects.all().order_by('-date_publishing')

    for limit in limits:
        tape_object_list = tape_object_list.exclude(limit, content_type=content_type)

    filterBySex = request.session.get('filterBySex', 0)
    if filterBySex != '0':
        tape_object_list = tape_object_list.filter(for_sex__in=[0, filterBySex])

    paginator, current_page = paginate_it(tape_object_list, request.GET.get('page'))

    # Рендер
    return {
        'important_articles': important_articles,
        'current_page': current_page,
        'paginator': paginator
    }


def choose_sex(request, sex):
    """
    Устанавливает пол в сессии. Редиректит на предыдущую страницу, если указана, иначе на главную.
    """
    request.session['filterBySex'] = sex

    return redirect(request.GET.get('from', 'main'))


# Просмотр статьи
@render_with_api.render_with_api('article.html')
def article(request, id):

    a = get_object_or_404(models.Article, id=id)

    return {
        'article_object': a
    }


@render_with_api.render_with_api('article_list.html')
def article_list(request, filterByRubricId='a', filterBySubRubricId='a'):

    important_articles = models.Article.objects.filter(is_important=True).order_by('-date_publishing')
    if filterByRubricId != 'a':
        important_articles = important_articles.filter(subrubric__rubric__id=filterByRubricId)
    if filterBySubRubricId != 'a':
        important_articles = important_articles.filter(subrubric__id=filterBySubRubricId)

    important_articles = important_articles[:4]

    # Вылезла проблема с MySQL: база не поддерживает оператор IN O_o ... приходится костылить
    limits = [~Q(id=i) for i in important_articles.values_list('id', flat=True)]

    articles = models.Article.objects.filter(*limits).order_by('-date_publishing')
    if filterByRubricId != 'a':
        articles = articles.filter(subrubric__rubric__id=filterByRubricId)
    if filterBySubRubricId != 'a':
        articles = articles.filter(subrubric__id=filterBySubRubricId)

    filterBySex = request.session.get('filterBySex', 0)
    if filterBySex != '0':
        articles = articles.filter(for_sex__in=[0, filterBySex])

    paginator, current_page = paginate_it(articles, request.GET.get('page'))

    # Рендер
    return {
        'important_articles': important_articles,
        'current_page': current_page,
        'paginator': paginator
    }


@render_with_api.render_with_api('blog_post.html')
def blog_post(request, id):
    bp = get_object_or_404(models.BlogPost, id=id)

    return {'article_object': bp}


@render_with_api.render_with_api('blog_post_list.html')
def blog_post_list(request):

    blog_post_list = models.BlogPost.objects.all().order_by('-date_publishing')

    filterBySex = request.session.get('filterBySex', 0)
    if filterBySex != '0':
        blog_post_list = blog_post_list.filter(for_sex__in=[0, filterBySex])

    paginator, current_page = paginate_it(blog_post_list, request.GET.get('page'))

    # Рендер
    return {
        'current_page': current_page,
        'paginator': paginator
    }


@render_with_api.render_with_api('news.html')
def news(request, id):
    news = get_object_or_404(models.ExternalNews, id=id, enabled=True)
    return {'article_object': news}


@render_with_api.render_with_api('news_list.html')
def news_list(request):
    news_list = models.ExternalNews.objects.filter(enabled=True).order_by('-date_publishing')

    filterBySex = request.session.get('filterBySex', 0)
    if filterBySex != '0':
        news_list = news_list.filter(for_sex__in=[0, filterBySex])

    paginator, current_page = paginate_it(news_list, request.GET.get('page'))

    # Рендер
    return {
        'current_page': current_page,
        'paginator': paginator
    }


@render_with_api.render_with_api('life.html')
def life(request):
    images = models.InstagramImage.objects.filter(is_accepted=True).order_by('-instagram_id')

    paginator, current_page = paginate_it(images, request.GET.get('page'))

    # Рендер
    return {
        'current_page': current_page,
        'paginator': paginator
    }


# API сайта
def links(request):

    # Рендер
    return render(request, 'links.html')
