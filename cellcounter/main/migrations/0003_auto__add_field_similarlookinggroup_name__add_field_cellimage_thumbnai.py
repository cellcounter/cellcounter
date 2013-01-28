# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'SimilarLookingGroup.name'
        db.add_column('main_similarlookinggroup', 'name',
                      self.gf('django.db.models.fields.CharField')(default='default', max_length=100),
                      keep_default=False)

        # Adding field 'CellImage.thumbnail_left'
        db.add_column('main_cellimage', 'thumbnail_left',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'CellImage.thumbnail_top'
        db.add_column('main_cellimage', 'thumbnail_top',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'CellImage.thumbnail_width'
        db.add_column('main_cellimage', 'thumbnail_width',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'SimilarLookingGroup.name'
        db.delete_column('main_similarlookinggroup', 'name')

        # Deleting field 'CellImage.thumbnail_left'
        db.delete_column('main_cellimage', 'thumbnail_left')

        # Deleting field 'CellImage.thumbnail_top'
        db.delete_column('main_cellimage', 'thumbnail_top')

        # Deleting field 'CellImage.thumbnail_width'
        db.delete_column('main_cellimage', 'thumbnail_width')


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
        'main.bonemarrowbackground': {
            'Meta': {'object_name': 'BoneMarrowBackground'},
            'cell_count_instance': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['main.CellCountInstance']", 'unique': 'True'}),
            'ease_of_aspiration': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'haemodilution': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'particle_cellularity': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'particulate': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'site': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'trail_cellularity': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'main.cellcount': {
            'Meta': {'object_name': 'CellCount'},
            'abnormal_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'cell': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.CellType']"}),
            'cell_count_instance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.CellCountInstance']"}),
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'normal_count': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'main.cellcountinstance': {
            'Meta': {'object_name': 'CellCountInstance'},
            'datetime_submitted': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'datetime_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'overall_comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'tissue_type': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'main.cellimage': {
            'Meta': {'object_name': 'CellImage'},
            'celltype': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.CellType']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'file': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'thumbnail_left': ('django.db.models.fields.IntegerField', [], {}),
            'thumbnail_top': ('django.db.models.fields.IntegerField', [], {}),
            'thumbnail_width': ('django.db.models.fields.IntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'main.celltype': {
            'Meta': {'object_name': 'CellType'},
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'machine_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'readable_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'visualisation_colour': ('colorful.fields.RGBColorField', [], {'max_length': '7', 'blank': 'True'})
        },
        'main.erythropoiesisfindings': {
            'Meta': {'object_name': 'ErythropoiesisFindings'},
            'cell_count_instance': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['main.CellCountInstance']", 'unique': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'megaloblastic_change': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'multinucleated_forms': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'no_dysplasia': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'nuclear_asynchrony': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ragged_haemoglobinisation': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'main.granulopoiesisfindings': {
            'Meta': {'object_name': 'GranulopoiesisFindings'},
            'cell_count_instance': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['main.CellCountInstance']", 'unique': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'dohle_bodies': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'hypogranular': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'no_dysplasia': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'nuclear_atypia': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'pelger': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'main.ironstain': {
            'Meta': {'object_name': 'IronStain'},
            'cell_count_instance': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['main.CellCountInstance']", 'unique': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iron_content': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'ringed_sideroblasts': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'stain_performed': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'main.megakaryocytefeatures': {
            'Meta': {'object_name': 'MegakaryocyteFeatures'},
            'cell_count_instance': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['main.CellCountInstance']", 'unique': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'fragmented': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'hypolobulated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'micromegakaryocytes': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'no_dysplasia': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'relative_count': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'main.similarlookinggroup': {
            'Meta': {'object_name': 'SimilarLookingGroup'},
            'cell_image': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['main.CellImage']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['main']