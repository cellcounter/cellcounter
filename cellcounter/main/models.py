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
    datetime_submitted = models.DateTimeField(auto_now_add=True)
    datetime_updated = models.DateTimeField(auto_now=True)
    tissue_type = models.CharField(max_length=25, choices=TISSUE_TYPE)
    overall_comment = models.TextField(blank=True)

    def __unicode__(self):
        return u'Count %s' %(self.id)

class BoneMarrowBackground(models.Model):
    cell_count_instance = models.OneToOneField(CellCountInstance)
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
    comment = models.TextField(blank=True)

class CellCount(models.Model):
    cell_count_instance = models.ForeignKey(CellCountInstance)
    cell = models.ForeignKey(CellType)
    normal_count = models.IntegerField()
    abnormal_count = models.IntegerField()
    comment = models.TextField(blank=True)

    def percentage(self):
        total = 0
        count_list = self.cell_count_instance.cellcount_set.all()
        for count in count_list:
            total = total + count.normal_count + count.abnormal_count

        if total != 0:
            return 100 * float(self.normal_count+self.abnormal_count)/float(total)
        else:
            return 0

class ErythropoiesisFindings(models.Model):
    cell_count_instance = models.OneToOneField(CellCountInstance)
    dysplasia = models.CharField(max_length=50,
                                choices=ERYTHROPOIESIS_DYSPLASIA)
    comment = models.TextField(blank=True)

class GranulopoiesisFindings(models.Model):
    cell_count_instance = models.OneToOneField(CellCountInstance)
    dysplasia = models.CharField(max_length=50,
                                choices=GRANULOPOIESIS_DYSPLASIA)
    comment = models.TextField(blank=True)

class MegakaryocyteFeatures(models.Model):
    cell_count_instance = models.OneToOneField(CellCountInstance)
    relative_count = models.CharField(max_length=50,
                                choices=MEGAKARYOCYTE_RELATIVE_COUNT)
    dysplasia = models.CharField(max_length=50,
                                choices=MEGAKARYOCYTE_DYSPLASIA)
    comment = models.TextField(blank=True)
