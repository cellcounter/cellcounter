from django.db import models
from django.contrib.auth.models import User

TISSUE_TYPE = (
        ('Blood film', 'Blood film'),
        ('Bone marrow', 'Bone marrow'))

CELLULARITY_CHOICES = (
        ('Hypo', 'Hypo'),
        ('Normal', 'Normal'),
        ('Hyper', 'Hyper'),
        ('Acellular', 'Acellular'))

BM_PARTICULATE = (
        ('No particles', 'No particles'),
        ('Few particles', 'Few particles'),
        ('Adequate particles', 'Adequate particles'))

BM_HAEMODILUTION =(
        ('Mild', 'Mild'),
        ('Moderate', 'Moderate'),
        ('Severe', 'Severe'),)

BM_EASE_OF_ASPIRATION = (
        ('Dry', 'Dry'),
        ('Easy', 'Easy'),
        ('Moderate', 'Moderate'),
        ('Hard', 'Hard'),
        ('Indeterminate', 'Indeterminate'))

ERYTHROPOIESIS_DYSPLASIA = (
        ('None', 'None'),
        ('Nuclear asynchrony', 'Nuclear asynchrony'),
        ('Multinucleated Forms', 'Multinucleated Forms'),
        ('Ragged haemoglobinisation', 'Ragged haemoglobinisation'),
        ('Megaloblastic change', 'Megaloblastic change'))

MEGAKARYOCYTE_RELATIVE_COUNT = (
        ('Absent', 'Absent'),
        ('Reduced', 'Reduced'),
        ('Normal', 'Normal'),
        ('Increased', 'Increased'))

MEGAKARYOCYTE_DYSPLASIA = (
        ('None', 'None'),
        ('Hypolobulated', 'Hypolobulated'),
        ('Fragmented', 'Fragmented'))

GRANULOPOIESIS_DYSPLASIA = (
        ('None', 'None'),
        ('Hypogranular', 'Hypogranular'),
        ('Pelger', 'Pelger'),
        ('Nuclear atypia', 'Nuclear atypia'),
        ('Dohle bodies', 'Dohle bodies'))

class CellCountInstance(models.Model):

    user = models.ForeignKey(User)
    datetime_submitted = models.DateTimeField()
    datetime_updated = models.DateTimeField()
    tissue_type = models.CharField(max_length=25, choices=TISSUE_TYPE)
    overall_comment = models.TextField()

    def __unicode__(self):
        return u'Count %s' %(self.id)

class BoneMarrowBackground(models.Model):
    cell_count_instance = models.ForeignKey(CellCountInstance)
    trail_cellularity = models.CharField(max_length=50,
                                        choices=CELLULARITY_CHOICES)
    particle_cellularity = models.CharField(max_length=50,
                                        choices=CELLULARITY_CHOICES)
    particulate = models.CharField(max_length=50,
                                choices=BM_PARTICULATE)
    haemodilution = models.CharField(max_length=50,
                                    choices=BM_HAEMODILUTION)
    site = models.CharField(max_length=50)
    ease_of_aspiration = models.CharField(max_length=50,
                                        choices=BM_EASE_OF_ASPIRATION)

class CellType(models.Model):
    readable_name = models.CharField(max_length=50)
    machine_name = models.CharField(max_length=50)
    comment = models.TextField()

class CellCount(models.Model):
    cell_count_instance = models.ForeignKey(CellCountInstance)
    cell = models.ForeignKey(CellType)
    count = models.IntegerField()
    comment = models.TextField(blank=True)

class ErythropoiesisFindings(models.Model):
    cell_count_instance = models.ForeignKey(CellCountInstance)
    dysplasia = models.CharField(max_length=50,
                                choices=ERYTHROPOIESIS_DYSPLASIA)
    comment = models.TextField()

class GranulopoiesisFindings(models.Model):
    cell_count_instance = models.ForeignKey(CellCountInstance)
    dysplasia = models.CharField(max_length=50,
                                choices=GRANULOPOIESIS_DYSPLASIA)
    comment = models.TextField()

