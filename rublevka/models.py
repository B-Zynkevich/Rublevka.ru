# -*- coding: utf-8 -*-

from django.db import models
from instagram.client import InstagramAPI
from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.core.urlresolvers import reverse
import re

# Статья/новость для
FOR_SEX_MAN = 1
FOR_SEX_WOMAN = 2
FOR_SEX = (
    (0, u'Унисекс'),
    (FOR_SEX_MAN, u'Для мужчин'),
    (FOR_SEX_WOMAN, u'Для женщин'),
)

# Все наследники models.Model будут иметь свойство с названием класса.
# Требуется для различения в шаблонах типа статьи
models.Model.class_name = property(lambda self: self.__class__.__name__)


class Tag(models.Model):
    name = models.CharField(max_length=256)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'Тэг'
        verbose_name_plural = u'Тэги'


# Рубрики. Используются для группировки подрубрик.
class Rubric(models.Model):
    name = models.CharField(verbose_name=u'Название', max_length=256)
    position = models.PositiveIntegerField(verbose_name=u'Порядок сортировки', )

    # Флаг что рубрика должна выводиться в верстке в пункте меню "Еще"
    in_more = models.BooleanField(verbose_name=u'Еще', default=True,
                                  help_text=u'Поставьте галку для отображения этого пункта меню в списке "Еще" на сайте')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'Рубрика'
        verbose_name_plural = u'Рубрики'
        ordering = ['position', ]


# Подрубрики. Каждая статья обязательно относится к одной из подрубрик.
# А каждая подрубрика обязательно находится в одной из рубрик.
# Так образуется древовидная структура.
class SubRubric(models.Model):
    name = models.CharField(verbose_name=u'Название', max_length=256)
    rubric = models.ForeignKey(Rubric, null=False, related_name='subrubrics')
    position = models.PositiveIntegerField(verbose_name=u'Порядок сортировки')

    # Если у рубрики несколько подрубрик, то полным именем будет имя рубрики + подрубрики.
    # Если у рубрики одна подрубрика, то их имена совпадают, в этом случае выводим только имя рубрики.
    @property
    def fullname(self):
        return self.rubric.name if self.rubric.name == self.name else u"{0} – {1}".format(self.rubric.name, self.name)

    def __unicode__(self):
        return self.fullname

    class Meta:
        verbose_name = u'Подрубрика'
        verbose_name_plural = u'Подрубрики'
        ordering = ['rubric', 'position', ]


class Article(models.Model):

    header = models.TextField(verbose_name=u"Заголовок")
    date_publishing = models.DateTimeField(verbose_name=u"Дата публикации")
    photo = models.FileField(verbose_name=u"Изображение", upload_to="article_photo")
    short_descr = models.CharField(verbose_name=u"Краткое описание для главной", max_length=1024, blank=True)
    content = models.TextField(verbose_name=u"Содержимое статьи")
    is_important = models.BooleanField(default=False, db_index=True, verbose_name=u"Важная статья")

    # Классификация.
    subrubric = models.ForeignKey(SubRubric, verbose_name=u"Подрубрика")
    tags = models.ManyToManyField(Tag, verbose_name=u"Тэги")
    for_sex = models.IntegerField(verbose_name=u"Для кого", default=0, db_index=True, choices=FOR_SEX)

    # Это свойство возвращает True для мужского пола и False для женского и None для унисекс.
    # Используется в django шаблоне для выбора класса.
    @property
    def for_sex_yesno(self):
        try:
            return {1: True, 2: False, 0: None}[self.for_sex]
        except:
            raise RuntimeError(u"Некорректное значение")

    def __unicode__(self):
        return self.header

    class Meta:
        verbose_name = u"Статья"
        verbose_name_plural = u"Статьи"

    def save(self, *args, **kwargs):

        creation = True if not self.id else False

        super(Article, self).save(*args, **kwargs)

        # Создаем запись в главной ленте
        content_type = ContentType.objects.get_for_model(self)

        if creation:
            MainTape.objects.create(date_publishing=self.date_publishing,
                                    for_sex=self.for_sex,
                                    content_type=content_type,
                                    object_id=self.id)


class Author(models.Model):
    first_name = models.CharField(max_length=20, null=False, blank=False, verbose_name=u'Имя')
    last_name = models.CharField(max_length=20, null=False, blank=False, verbose_name=u'Фамилия')
    photo = models.ImageField(upload_to="authors", null=True, blank=True)

    class Meta:
        verbose_name = u'Автор'
        verbose_name_plural = u'Авторы'

    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.last_name)


class BlogPost(models.Model):
    author = models.ForeignKey(Author, null=False, blank=False, verbose_name=u'Автор')
    title = models.CharField(max_length=500, verbose_name=u'Название', null=False, blank=False)
    content = models.TextField(verbose_name=u'Содержимое', null=True, blank=True)
    tags = models.ManyToManyField(Tag, null=True, blank=True)
    date_publishing = models.DateTimeField(auto_now_add=True, verbose_name=u"Дата публикации")
    for_sex = models.IntegerField(verbose_name=u"Для кого", default=0, db_index=True, choices=FOR_SEX)

    # Это свойство возвращает True для мужского пола и False для женского и None для унисекс.
    # Используется в django шаблоне для выбора класса.
    @property
    def for_sex_yesno(self):
        try:
            return {1: True, 2: False, 0: None}[self.for_sex]
        except:
            raise RuntimeError(u"Некорректное значение")

    class Meta:
        verbose_name = u'Запись в блоге'
        verbose_name_plural = u'Записи в блоге'

    def __unicode__(self):
        return u'%s "%s"' % (self.author, self.title[:30])

    @property
    def previous_post(self):
        model = self.__class__
        if model.objects.filter(id__lt=self.id).exists():
            return model.objects.filter(id__lt=self.id).order_by('-id')[0]
        else:
            return None

    @property
    def next_post(self):
        model = self.__class__
        if model.objects.filter(id__gt=self.id).exists():
            return model.objects.filter(id__gt=self.id).order_by('id')[0]
        else:
            return None

    def save(self, *args, **kwargs):

        creation = True if not self.id else False

        super(BlogPost, self).save(*args, **kwargs)

        # Создаем запись в главной ленте
        content_type = ContentType.objects.get_for_model(self)

        if creation:
            MainTape.objects.create(date_publishing=self.date_publishing,
                                    for_sex=self.for_sex,
                                    content_type=content_type,
                                    object_id=self.id)


class ExternalNews(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False, verbose_name=u'Название')
    link = models.CharField(max_length=255, null=False, blank=False, verbose_name=u'Ссылка')
    description = models.TextField(null=True, blank=True, verbose_name=u'Описание')
    date_publishing = models.DateTimeField(null=True, blank=True, db_column="pubdate", verbose_name=u'Дата публикации')
    media_content = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'Медиа контент')
    content = models.TextField(null=True, blank=True, verbose_name=u'Содержимое')
    enabled = models.BooleanField(default=False, db_index=True, verbose_name=u'Опубликована')
    news_hash = models.CharField(max_length=255, null=False, blank=False, db_column="hash", db_index=True, verbose_name=u'Хэш')
    for_sex = models.IntegerField(verbose_name=u"Для кого", default=0, db_index=True, choices=FOR_SEX)
    photo = models.FileField(verbose_name=u"Изображение", upload_to="external_news_photo", null=True, blank=True)

    class Meta:
        verbose_name = u'Новость из внешнего источника'
        verbose_name_plural = u'Новости из внешних источников'
        db_table = "external_news"
        ordering = ('-date_publishing',)

    def __unicode__(self):
        return self.title

    @property
    def for_sex_yesno(self):
        try:
            return {1: True, 2: False, 0: None}[self.for_sex]
        except:
            raise RuntimeError(u"Некорректное значение")

    def save(self, *args, **kwargs):
        super(ExternalNews, self).save(*args, **kwargs)

        # Создаем запись в главной ленте
        content_type = ContentType.objects.get_for_model(self)

        if self.enabled:
            if not MainTape.objects.filter(content_type=content_type, object_id=self.id).exists():
                MainTape.objects.create(date_publishing=self.date_publishing,
                                        for_sex=self.for_sex,
                                        content_type=content_type,
                                        object_id=self.id)
        else:
            if MainTape.objects.filter(content_type=content_type, object_id=self.id).exists():
                MainTape.objects.filter(content_type=content_type, object_id=self.id).delete()


class MainTape(models.Model):

    """ Модель, аггрегирующая в себе три сущности: статьи, новости и блоги.
        Служит для вывода всех этих сущностей на главную страницу по мере их опубликования.
        Облегчает паггинацию, так как паггинация производится по одной выборке, а не по трем.
        Использует джанговский механизм Generic Relations https://docs.djangoproject.com/en/1.5/ref/contrib/contenttypes/#id1
    """
    date_publishing = models.DateTimeField(null=True, blank=True, verbose_name=u'Дата публикации')
    for_sex = models.IntegerField(default=0, db_index=True, choices=FOR_SEX)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')


class InstagramAccount(models.Model):
    instagram_id = models.BigIntegerField(null=False, unique=True, verbose_name=u'ID пользователя в Instagram')
    username = models.CharField(max_length=100, null=False, blank=False, verbose_name=u'Логин')
    full_name = models.CharField(max_length=200, null=False, blank=False, verbose_name=u'Полное имя')
    profile_picture = models.URLField(max_length=300, null=True, blank=True, verbose_name=u'Фото')

    class Meta:
        verbose_name = u'Аккаунт Instagram'
        verbose_name_plural = u'Аккаунты Instagram'

    def __unicode__(self):
        return self.full_name

    def clean(self):
        """ При сохранении проверяем существование аккаунта и получаем инфу о нем из Instagram"""

        api = InstagramAPI(client_id=settings.INSTAGRAM_CLIENT_ID, client_secret=settings.INSTAGRAM_CLIENT_SECRET)
        user = api.user_search(self.username, 1)

        # Поиск ведется по четкому совпадению введенного имени
        if len(user) == 0 or self.username != user[0].username:
            raise ValidationError(u'Пользователя с таким именем не существует')

        self.instagram_id = user[0].id
        self.full_name = user[0].full_name
        self.profile_picture = user[0].profile_picture

    @property
    def latest_image(self):
        if self.images.exists():
            return self.images.order_by('-instagram_id')[0]
        return None

    @property
    def profile_link(self):
        """ Ссылка на профиль пользователя в Instagram """
        return 'http://instagram.com/%s' % self.username


class InstagramImage(models.Model):
    account = models.ForeignKey(InstagramAccount, null=False, related_name='images', verbose_name=u'Автор')
    instagram_id = models.BigIntegerField(null=False, unique=True, verbose_name=u'ID изображения в Instagram')
    instagram_link = models.URLField(max_length=300, null=True, blank=True, verbose_name=u'URL изображения в Instagram')
    url = models.URLField(max_length=300, null=True, blank=True, verbose_name=u'Адрес изображения')
    is_accepted = models.BooleanField(default=False, db_index=True, verbose_name=u'Допущено на сайт')

    class Meta:
        verbose_name = u'Изображение из Instagram'
        verbose_name_plural = u'Изображения из Instagram'


def _getCurrentFilterStateFromRequest(request):

        # Если текущий УРЛ - фильтр, тогда из УРЛа берем текущие значения для фильтра рубрики, подрубрики.
        # УРЛ должен иметь формат: /articles/r/N/sr/N/ где вместо N - значение фильтра соответственно
        # рубрика, подрубрика. В качестве значения "все" используется буква "а" (all).
        pattern = re.compile('^/articles/r/(?P<filterByRubricId>\d+|a)/sr/(?P<filterBySubRubricId>\d+|a)/$')
        matches = pattern.match(request.path.lower())

        if matches:
            return {
                'currentRubricId': matches.groupdict()['filterByRubricId'],
                'currentSubRubricId': matches.groupdict()['filterBySubRubricId']
            }

        return {
            'currentRubricId': 'a',
            'currentSubRubricId': 'a'
        }


# Класс для итерации по пунктам меню - рубрикам чтобы вычислять УРЛы для фильтров и активность пунктов.
class RubricMenu(object):

    # Инициализируем request (чтобы вычислить текущее состояние) и rubrics (чтобы получить инфо по всем рубрикам)
    def __init__(self, request, rubrics):

        # Текущее состояние всего меню рубрик (какие фильтры включены)
        self.currentState = _getCurrentFilterStateFromRequest(request)

        # Дерево рубрик-подрубрик и текущее состояние каждой из них
        # Используется для генерации верстки меню в шаблоне.
        self.rubrics = []
        for r in rubrics:
            self.rubrics.append(
                {
                    'id': r.id,
                    'name': r.name,
                    'is_current': str(r.id) == self.currentState['currentRubricId'],
                    'url': reverse('rubric', args=(r.id, 'a')),
                    'subrubrics': None,
                }
            )

            # Возвращает непустоту в subrubrics только для случая когда подрубрик >= 2.
            # Если подрубрик 1, в этом случае подпункты для рубрики делать в верстке не надо.
            if r.subrubrics.count() >= 2:
                self.rubrics[-1]['subrubrics'] = []
                for sr in r.subrubrics.all().order_by('position'):
                    self.rubrics[-1]['subrubrics'].append(
                        {
                            'id': sr.id,
                            'name': sr.name,
                            'is_current': str(sr.id) == self.currentState['currentSubRubricId'],
                            'url': reverse('rubric', args=(r.id, sr.id)),
                        }
                    )

    # Перебор рубрик
    def __iter__(self):
        return self.rubrics.__iter__()


# Контекстный процессор для Джанги для создания главного меню (список рубрик)
def mainMenuContextProcessor(request):
    return {
        "mainMenu": RubricMenu(request, Rubric.objects.filter(in_more=False).order_by('position')),
        "mainMenuMore": RubricMenu(request, Rubric.objects.filter(in_more=True).order_by('position')),
        "sexFilter": int(request.session.get('filterBySex', 0))
    }
