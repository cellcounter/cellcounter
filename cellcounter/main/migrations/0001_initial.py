# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CellCountInstance'
        db.create_table('main_cellcountinstance', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('datetime_submitted', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('datetime_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('tissue_type', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('overall_comment', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('main', ['CellCountInstance'])

        # Adding model 'BoneMarrowBackground'
        db.create_table('main_bonemarrowbackground', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cell_count_instance', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['main.CellCountInstance'], unique=True)),
            ('trail_cellularity', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('particle_cellularity', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('particulate', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('haemodilution', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('site', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('ease_of_aspiration', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('main', ['BoneMarrowBackground'])

        # Adding model 'CellType'
        db.create_table('main_celltype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('readable_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('machine_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('comment', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('main', ['CellType'])

        # Adding model 'CellCount'
        db.create_table('main_cellcount', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cell_count_instance', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.CellCountInstance'])),
            ('cell', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.CellType'])),
            ('normal_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('abnormal_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('comment', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('main', ['CellCount'])

        # Adding model 'ErythropoiesisFindings'
        db.create_table('main_erythropoiesisfindings', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cell_count_instance', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['main.CellCountInstance'], unique=True)),
            ('no_dysplasia', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('nuclear_asynchrony', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('multinucleated_forms', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('ragged_haemoglobinisation', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('megaloblastic_change', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('comment', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('main', ['ErythropoiesisFindings'])

        # Adding model 'GranulopoiesisFindings'
        db.create_table('main_granulopoiesisfindings', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cell_count_instance', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['main.CellCountInstance'], unique=True)),
            ('no_dysplasia', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('hypogranular', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('pelger', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('nuclear_atypia', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('dohle_bodies', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('comment', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('main', ['GranulopoiesisFindings'])

        # Adding model 'MegakaryocyteFeatures'
        db.create_table('main_megakaryocytefeatures', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cell_count_instance', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['main.CellCountInstance'], unique=True)),
            ('relative_count', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('no_dysplasia', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('hypolobulated', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('fragmented', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('micromegakaryocytes', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('comment', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('main', ['MegakaryocyteFeatures'])

        # Adding model 'IronStain'
        db.create_table('main_ironstain', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cell_count_instance', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['main.CellCountInstance'], unique=True)),
            ('stain_performed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('iron_content', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('ringed_sideroblasts', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('main', ['IronStain'])

        # Adding model 'CellImage'
        db.create_table('main_cellimage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('file', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('celltype', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.CellType'])),
        ))
        db.send_create_signal('main', ['CellImage'])

        # Adding model 'SimilarLookingGroup'
        db.create_table('main_similarlookinggroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('main', ['SimilarLookingGroup'])

        # Adding M2M table for field cell_image on 'SimilarLookingGroup'
        db.create_table('main_similarlookinggroup_cell_image', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('similarlookinggroup', models.ForeignKey(orm['main.similarlookinggroup'], null=False)),
            ('cellimage', models.ForeignKey(orm['main.cellimage'], null=False))
        ))
        db.create_unique('main_similarlookinggroup_cell_image', ['similarlookinggroup_id', 'cellimage_id'])


    def backwards(self, orm):
        # Deleting model 'CellCountInstance'
        db.delete_table('main_cellcountinstance')

        # Deleting model 'BoneMarrowBackground'
        db.delete_table('main_bonemarrowbackground')

        # Deleting model 'CellType'
        db.delete_table('main_celltype')

        # Deleting model 'CellCount'
        db.delete_table('main_cellcount')

        # Deleting model 'ErythropoiesisFindings'
        db.delete_table('main_erythropoiesisfindings')

        # Deleting model 'GranulopoiesisFindings'
        db.delete_table('main_granulopoiesisfindings')

        # Deleting model 'MegakaryocyteFeatures'
        db.delete_table('main_megakaryocytefeatures')

        # Deleting model 'IronStain'
        db.delete_table('main_ironstain')

        # Deleting model 'CellImage'
        db.delete_table('main_cellimage')

        # Deleting model 'SimilarLookingGroup'
        db.delete_table('main_similarlookinggroup')

        # Removing M2M table for field cell_image on 'SimilarLookingGroup'
        db.delete_table('main_similarlookinggroup_cell_image')


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
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'main.celltype': {
            'Meta': {'object_name': 'CellType'},
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'machine_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'readable_name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['main']