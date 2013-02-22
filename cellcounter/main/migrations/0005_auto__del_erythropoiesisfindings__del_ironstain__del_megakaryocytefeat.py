# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'ErythropoiesisFindings'
        db.delete_table('main_erythropoiesisfindings')

        # Deleting model 'IronStain'
        db.delete_table('main_ironstain')

        # Deleting model 'MegakaryocyteFeatures'
        db.delete_table('main_megakaryocytefeatures')

        # Deleting model 'CellCount'
        db.delete_table('main_cellcount')

        # Deleting model 'CellCountInstance'
        db.delete_table('main_cellcountinstance')

        # Deleting model 'BoneMarrowBackground'
        db.delete_table('main_bonemarrowbackground')

        # Deleting model 'GranulopoiesisFindings'
        db.delete_table('main_granulopoiesisfindings')


    def backwards(self, orm):
        
        # Adding model 'ErythropoiesisFindings'
        db.create_table('main_erythropoiesisfindings', (
            ('comment', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('megaloblastic_change', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('nuclear_asynchrony', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('no_dysplasia', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('ragged_haemoglobinisation', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('cell_count_instance', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['main.CellCountInstance'], unique=True)),
            ('multinucleated_forms', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('main', ['ErythropoiesisFindings'])

        # Adding model 'IronStain'
        db.create_table('main_ironstain', (
            ('comment', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('stain_performed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('iron_content', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ringed_sideroblasts', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('cell_count_instance', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['main.CellCountInstance'], unique=True)),
        ))
        db.send_create_signal('main', ['IronStain'])

        # Adding model 'MegakaryocyteFeatures'
        db.create_table('main_megakaryocytefeatures', (
            ('comment', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('fragmented', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('relative_count', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('no_dysplasia', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('hypolobulated', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('micromegakaryocytes', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('cell_count_instance', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['main.CellCountInstance'], unique=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('main', ['MegakaryocyteFeatures'])

        # Adding model 'CellCount'
        db.create_table('main_cellcount', (
            ('comment', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cell', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.CellType'])),
            ('normal_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('cell_count_instance', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.CellCountInstance'])),
            ('abnormal_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('main', ['CellCount'])

        # Adding model 'CellCountInstance'
        db.create_table('main_cellcountinstance', (
            ('datetime_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('overall_comment', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('datetime_submitted', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tissue_type', self.gf('django.db.models.fields.CharField')(max_length=25)),
        ))
        db.send_create_signal('main', ['CellCountInstance'])

        # Adding model 'BoneMarrowBackground'
        db.create_table('main_bonemarrowbackground', (
            ('site', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('haemodilution', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('trail_cellularity', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('particle_cellularity', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('particulate', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('cell_count_instance', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['main.CellCountInstance'], unique=True)),
            ('ease_of_aspiration', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('main', ['BoneMarrowBackground'])

        # Adding model 'GranulopoiesisFindings'
        db.create_table('main_granulopoiesisfindings', (
            ('comment', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('no_dysplasia', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('pelger', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nuclear_atypia', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('hypogranular', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('cell_count_instance', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['main.CellCountInstance'], unique=True)),
            ('dohle_bodies', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('main', ['GranulopoiesisFindings'])


    models = {
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
            'abbr_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'machine_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'readable_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'visualisation_colour': ('colorful.fields.RGBColorField', [], {'max_length': '7', 'blank': 'True'})
        },
        'main.similarlookinggroup': {
            'Meta': {'object_name': 'SimilarLookingGroup'},
            'cell_image': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['main.CellImage']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['main']
