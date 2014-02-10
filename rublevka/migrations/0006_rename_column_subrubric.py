# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        db.rename_column(u'rublevka_article', u'rubric_id', u'subrubric_id')

    def backwards(self, orm):
        db.rename_column(u'rublevka_article', u'subrubric_id', u'rubric_id')

    models = {
        u'rublevka.article': {
            'Meta': {'object_name': 'Article'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'date_publishing': ('django.db.models.fields.DateTimeField', [], {}),
            'for_sex': ('django.db.models.fields.IntegerField', [], {}),
            'header': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photo': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'short_descr': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'subrubric': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['rublevka.SubRubric']"}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['rublevka.Tag']", 'symmetrical': 'False'})
        },
        u'rublevka.rubricgroup': {
            'Meta': {'object_name': 'RubricGroup'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'rublevka.subrubric': {
            'Meta': {'object_name': 'SubRubric'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'rubric_group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['rublevka.RubricGroup']"})
        },
        u'rublevka.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        }
    }

    complete_apps = ['rublevka']