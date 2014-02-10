# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Tag'
        db.create_table(u'rublevka_tag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal(u'rublevka', ['Tag'])

        # Adding model 'Rubric'
        db.create_table(u'rublevka_rubric', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal(u'rublevka', ['Rubric'])

        # Adding model 'Article'
        db.create_table(u'rublevka_article', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('header', self.gf('django.db.models.fields.TextField')()),
            ('date_publishing', self.gf('django.db.models.fields.DateTimeField')()),
            ('photo', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('short_descr', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('rubric', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rublevka.Rubric'])),
        ))
        db.send_create_signal(u'rublevka', ['Article'])

        # Adding M2M table for field tags on 'Article'
        m2m_table_name = db.shorten_name(u'rublevka_article_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('article', models.ForeignKey(orm[u'rublevka.article'], null=False)),
            ('tag', models.ForeignKey(orm[u'rublevka.tag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['article_id', 'tag_id'])


    def backwards(self, orm):
        # Deleting model 'Tag'
        db.delete_table(u'rublevka_tag')

        # Deleting model 'Rubric'
        db.delete_table(u'rublevka_rubric')

        # Deleting model 'Article'
        db.delete_table(u'rublevka_article')

        # Removing M2M table for field tags on 'Article'
        db.delete_table(db.shorten_name(u'rublevka_article_tags'))


    models = {
        u'rublevka.article': {
            'Meta': {'object_name': 'Article'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'date_publishing': ('django.db.models.fields.DateTimeField', [], {}),
            'header': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photo': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'rubric': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['rublevka.Rubric']"}),
            'short_descr': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['rublevka.Tag']", 'symmetrical': 'False'})
        },
        u'rublevka.rubric': {
            'Meta': {'object_name': 'Rubric'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'rublevka.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        }
    }

    complete_apps = ['rublevka']