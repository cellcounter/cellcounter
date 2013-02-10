# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'License'
        db.create_table('main_license', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('details', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('main', ['License'])

        # Adding model 'CopyrightHolder'
        db.create_table('main_copyrightholder', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=300)),
        ))
        db.send_create_signal('main', ['CopyrightHolder'])

        # Adding M2M table for field user on 'CopyrightHolder'
        db.create_table('main_copyrightholder_user', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('copyrightholder', models.ForeignKey(orm['main.copyrightholder'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('main_copyrightholder_user', ['copyrightholder_id', 'user_id'])

        # Adding field 'CellImage.uploader'
        db.add_column('main_cellimage', 'uploader',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'CellImage.copyright'
        db.add_column('main_cellimage', 'copyright',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['main.CopyrightHolder']),
                      keep_default=False)

        # Adding field 'CellImage.license'
        db.add_column('main_cellimage', 'license',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['main.License']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'License'
        db.delete_table('main_license')

        # Deleting model 'CopyrightHolder'
        db.delete_table('main_copyrightholder')

        # Removing M2M table for field user on 'CopyrightHolder'
        db.delete_table('main_copyrightholder_user')

        # Deleting field 'CellImage.uploader'
        db.delete_column('main_cellimage', 'uploader_id')

        # Deleting field 'CellImage.copyright'
        db.delete_column('main_cellimage', 'copyright_id')

        # Deleting field 'CellImage.license'
        db.delete_column('main_cellimage', 'license_id')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'main.cellimage': {
            'Meta': {'object_name': 'CellImage'},
            'celltype': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.CellType']"}),
            'copyright': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.CopyrightHolder']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'file': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'license': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.License']"}),
            'thumbnail_left': ('django.db.models.fields.IntegerField', [], {}),
            'thumbnail_top': ('django.db.models.fields.IntegerField', [], {}),
            'thumbnail_width': ('django.db.models.fields.IntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'uploader': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'main.celltype': {
            'Meta': {'object_name': 'CellType'},
            'abbr_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'machine_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'readable_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'visualisation_colour': ('colorful.fields.RGBColorField', [], {'max_length': '7', 'blank': 'True'})
        },
        'main.copyrightholder': {
            'Meta': {'object_name': 'CopyrightHolder'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'user': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False'})
        },
        'main.license': {
            'Meta': {'object_name': 'License'},
            'details': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'main.similarlookinggroup': {
            'Meta': {'object_name': 'SimilarLookingGroup'},
            'cell_image': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['main.CellImage']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['main']