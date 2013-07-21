# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'KeyMap'
        db.create_table(u'keyboardapi_keymap', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cellid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.CellType'])),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal(u'keyboardapi', ['KeyMap'])

        # Adding model 'CustomKeyboard'
        db.create_table(u'keyboardapi_customkeyboard', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('is_primary', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'keyboardapi', ['CustomKeyboard'])

        # Adding unique constraint on 'CustomKeyboard', fields ['user', 'label']
        db.create_unique(u'keyboardapi_customkeyboard', ['user_id', 'label'])

        # Adding M2M table for field mappings on 'CustomKeyboard'
        m2m_table_name = db.shorten_name(u'keyboardapi_customkeyboard_mappings')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('customkeyboard', models.ForeignKey(orm[u'keyboardapi.customkeyboard'], null=False)),
            ('keymap', models.ForeignKey(orm[u'keyboardapi.keymap'], null=False))
        ))
        db.create_unique(m2m_table_name, ['customkeyboard_id', 'keymap_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'CustomKeyboard', fields ['user', 'label']
        db.delete_unique(u'keyboardapi_customkeyboard', ['user_id', 'label'])

        # Deleting model 'KeyMap'
        db.delete_table(u'keyboardapi_keymap')

        # Deleting model 'CustomKeyboard'
        db.delete_table(u'keyboardapi_customkeyboard')

        # Removing M2M table for field mappings on 'CustomKeyboard'
        db.delete_table(db.shorten_name(u'keyboardapi_customkeyboard_mappings'))


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'keyboardapi.customkeyboard': {
            'Meta': {'unique_together': "(('user', 'label'),)", 'object_name': 'CustomKeyboard'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_primary': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'mappings': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['keyboardapi.KeyMap']", 'symmetrical': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'keyboardapi.keymap': {
            'Meta': {'object_name': 'KeyMap'},
            'cellid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.CellType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        u'main.celltype': {
            'Meta': {'object_name': 'CellType'},
            'abbr_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'machine_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'readable_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'visualisation_colour': ('colorful.fields.RGBColorField', [], {'max_length': '7', 'blank': 'True'})
        }
    }

    complete_apps = ['keyboardapi']