# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'InstagramImage'
        db.create_table(u'rublevka_instagramimage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(related_name='images', to=orm['rublevka.InstagramAccount'])),
            ('instagram_id', self.gf('django.db.models.fields.BigIntegerField')(unique=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=300, null=True, blank=True)),
            ('is_accepted', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
        ))
        db.send_create_signal(u'rublevka', ['InstagramImage'])


        # Changing field 'InstagramAccount.instagram_id'
        db.alter_column(u'rublevka_instagramaccount', 'instagram_id', self.gf('django.db.models.fields.BigIntegerField')(unique=True))
        # Adding unique constraint on 'InstagramAccount', fields ['instagram_id']
        db.create_unique(u'rublevka_instagramaccount', ['instagram_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'InstagramAccount', fields ['instagram_id']
        db.delete_unique(u'rublevka_instagramaccount', ['instagram_id'])

        # Deleting model 'InstagramImage'
        db.delete_table(u'rublevka_instagramimage')


        # Changing field 'InstagramAccount.instagram_id'
        db.alter_column(u'rublevka_instagramaccount', 'instagram_id', self.gf('django.db.models.fields.IntegerField')())

    models = {
        u'rublevka.article': {
            'Meta': {'object_name': 'Article'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'date_publishing': ('django.db.models.fields.DateTimeField', [], {}),
            'for_sex': ('django.db.models.fields.IntegerField', [], {}),
            'header': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_important': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
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
            'date_publishing': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['rublevka.Tag']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'rublevka.externalnews': {
            'Meta': {'ordering': "('-date_publishing',)", 'object_name': 'ExternalNews', 'db_table': "'external_news'"},
            'content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'date_publishing': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'db_column': "'pubdate'", 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'for_sex': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'media_content': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'news_hash': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_column': "'hash'", 'db_index': 'True'}),
            'photo': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'rublevka.instagramaccount': {
            'Meta': {'object_name': 'InstagramAccount'},
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instagram_id': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True'}),
            'profile_picture': ('django.db.models.fields.URLField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'rublevka.instagramimage': {
            'Meta': {'object_name': 'InstagramImage'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'images'", 'to': u"orm['rublevka.InstagramAccount']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instagram_id': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True'}),
            'is_accepted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'})
        },
        u'rublevka.rubric': {
            'Meta': {'ordering': "['position']", 'object_name': 'Rubric'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_more': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'rublevka.subrubric': {
            'Meta': {'ordering': "['rubric', 'position']", 'object_name': 'SubRubric'},
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