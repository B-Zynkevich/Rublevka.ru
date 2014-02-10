#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Evgeniy Pokidov
# @Date:   2013-12-05 09:33:07
# @Email:  pokidovea@gmail.com
# @Last modified by:   pokidovea
# @Last Modified time: 2013-12-05 12:53:50

from django.test import TestCase
from django_any import any_model
from django.test.client import Client
import models


class RublevkaTest(TestCase):

    def setUp(self):

        self.client = Client()

        for i in xrange(100):
            any_model(models.Article)
            any_model(models.BlogPost)
            any_model(models.ExternalNews, enabled=True)

    def test_main_tape_items_count(self):
        self.assertEqual(models.MainTape.objects.count(), 300)

    def test_access_main_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_access_main_page_api(self):
        response = self.client.get('/?api')
        self.assertEqual(response.status_code, 200)

    def test_access_blogs(self):
        response = self.client.get('/blogs/')
        self.assertEqual(response.status_code, 200)

    def test_access_blogs_api(self):
        response = self.client.get('/blogs/?api')
        self.assertEqual(response.status_code, 200)

    def test_access_blog(self):
        blog = models.BlogPost.objects.all()[0]

        response = self.client.get('/blog/%s/' % blog.id)
        self.assertEqual(response.status_code, 200)

    def test_access_blog_api(self):
        blog = models.BlogPost.objects.all()[0]

        response = self.client.get('/blog/%s/?api' % blog.id)
        self.assertEqual(response.status_code, 200)

    def test_access_news_list(self):
        response = self.client.get('/news/')
        self.assertEqual(response.status_code, 200)

    def test_access_news_list_api(self):
        response = self.client.get('/news/?api')
        self.assertEqual(response.status_code, 200)

    def test_access_news(self):
        news = models.ExternalNews.objects.all()[0]

        response = self.client.get('/news/%s/' % news.id)
        self.assertEqual(response.status_code, 200)

    def test_access_news_api(self):
        news = models.ExternalNews.objects.all()[0]

        response = self.client.get('/news/%s/?api' % news.id)
        self.assertEqual(response.status_code, 200)

    def test_access_articles(self):
        response = self.client.get('/articles/')
        self.assertEqual(response.status_code, 200)

        subrubric = models.SubRubric.objects.all()[0]

        response = self.client.get('/articles/r/%s/sr/%s/' % (subrubric.rubric.id, subrubric.id))
        self.assertEqual(response.status_code, 200)

    def test_access_articles_api(self):
        response = self.client.get('/articles/?api')
        self.assertEqual(response.status_code, 200)

        subrubric = models.SubRubric.objects.all()[0]

        response = self.client.get('/articles/r/%s/sr/%s/?api' % (subrubric.rubric.id, subrubric.id))
        self.assertEqual(response.status_code, 200)

    def test_access_article(self):
        article = models.Article.objects.all()[0]

        response = self.client.get('/article/%s/' % article.id)
        self.assertEqual(response.status_code, 200)

    def test_access_article_api(self):
        article = models.Article.objects.all()[0]

        response = self.client.get('/article/%s/?api' % article.id)
        self.assertEqual(response.status_code, 200)

    def test_access_life(self):
        response = self.client.get('/life/')
        self.assertEqual(response.status_code, 200)

    def test_access_life_api(self):
        response = self.client.get('/life/?api')
        self.assertEqual(response.status_code, 200)
