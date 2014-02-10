# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Author'
        db.create_table(u'rublevka_author', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'rublevka', ['Author'])

        # Adding model 'BlogPost'
        db.create_table(u'rublevka_blogpost', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rublevka.Author'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('content', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'rublevka', ['BlogPost'])

        # Adding M2M table for field tags on 'BlogPost'
        m2m_table_name = db.shorten_name(u'rublevka_blogpost_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('blogpost', models.ForeignKey(orm[u'rublevka.blogpost'], null=False)),
            ('tag', models.ForeignKey(orm[u'rublevka.tag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['blogpost_id', 'tag_id'])


    def backwards(self, orm):
        # Deleting model 'Author'
        db.delete_table(u'rublevka_author')

        # Deleting model 'BlogPost'
        db.delete_table(u'rublevka_blogpost')

        # Removing M2M table for field tags on 'BlogPost'
        db.delete_table(db.shorten_name(u'rublevka_blogpost_tags'))


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
        u'rublevka.author': {
            'Meta': {'object_name': 'Author'},
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'rublevka.blogpost': {
            'Meta': {'object_name': 'BlogPost'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['rublevka.Author']"}),
            'content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['rublevka.Tag']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'rublevka.rubric': {
            'Meta': {'ordering': "['position']", 'object_name': 'Rubric'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'rublevka.subrubric': {
            'Meta': {'ordering': "['position']", 'object_name': 'SubRubric'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'rubric': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['rublevka.Rubric']"})
        },
        u'rublevka.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        }
    }

    complete_apps = ['rublevka']