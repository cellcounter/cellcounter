from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User

class CellCountInstance(models.Model):
    TISSUE_TYPE = (
        ('Blood film', 'Blood film'),
        ('Bone marrow', 'Bone marrow'))

    user = models.ForeignKey(User)
    datetime_submitted = models.DateTimeField(auto_now_add=True)
    datetime_updated = models.DateTimeField(auto_now=True)
    tissue_type = models.CharField(max_length=25, choices=TISSUE_TYPE)
    overall_comment = models.TextField(blank=True)

    def __unicode__(self):
        return u'Count ID #%s' %(self.id)

    def myeloid_erythroid_ratio(self):
        """Returns M/E ratio for a given count"""
        if not self.erythroid_cellcount():
            return 'Unable to calculate, erythroid count = 0'
        else:
            return round((float(self.myeloid_cellcount())/float(self.erythroid_cellcount())), 2)

    def total_cellcount(self):
        """Returns a total count of all cells in count"""
        total = 0
        for count in self.cellcount_set.all():
            total = total + count.get_total_count()
        return total

    def myeloid_cellcount(self):
        """Returns a total count of all myeloid cells in count"""
        total = 0
        for count in self.cellcount_set.filter(Q(cell__machine_name='blasts') | 
                                               Q(cell__machine_name='neutrophils') |
                                               Q(cell__machine_name='band_forms') |
                                               Q(cell__machine_name='myelocytes') |
                                               Q(cell__machine_name='promyelocytes') | 
                                               Q(cell__machine_name='basophils') |
                                               Q(cell__machine_name='eosinophils')):
            total = total + count.get_total_count()
        return total

    def erythroid_cellcount(self):
        """Returns a total count of all erythroid cells in count"""
        erythroid_count = self.cellcount_set.get(cell__machine_name='erythroid')
        total = erythroid_count.get_total_count()
        return total

class BoneMarrowBackground(models.Model):
    CELLULARITY_CHOICES = (('Hypo', 'Hypo'),
                           ('Normal', 'Normal'),
                           ('Hyper', 'Hyper'),
                           ('Acellular', 'Acellular'))
    BM_PARTICULATE = (('No particles', 'No particles'),
                      ('Few particles', 'Few particles'),
                      ('Adequate particles', 'Adequate particles'))
    BM_HAEMODILUTION =(('Mild', 'Mild'),
                       ('Moderate', 'Moderate'),
                       ('Severe', 'Severe'),)
    BM_EASE_OF_ASPIRATION = (('Dry', 'Dry'),
                             ('Easy', 'Easy'),
                             ('Moderate', 'Moderate'),
                             ('Hard', 'Hard'),
                             ('Indeterminate', 'Indeterminate'))

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
    machine_name = models.CharField(max_length=50, unique=True)
    comment = models.TextField(blank=True)

class CellCount(models.Model):
    cell_count_instance = models.ForeignKey(CellCountInstance)
    cell = models.ForeignKey(CellType)
    normal_count = models.IntegerField(default=0)
    abnormal_count = models.IntegerField(default=0)
    comment = models.TextField(blank=True)

    def get_total_count(self):
        return self.normal_count + self.abnormal_count

    def percentage(self):
        total = self.cell_count_instance.total_cellcount()
        if total != 0:
            return round((100 * float(self.normal_count+self.abnormal_count)/float(total)))
        else:
            return 0

class ErythropoiesisFindings(models.Model):
    ERYTHROPOIESIS_DYSPLASIA = (('None', 'None'),
            ('Nuclear asynchrony', 'Nuclear asynchrony'),
            ('Multinucleated Forms', 'Multinucleated Forms'),
            ('Ragged haemoglobinisation', 'Ragged haemoglobinisation'),
            ('Megaloblastic change', 'Megaloblastic change'))

    cell_count_instance = models.OneToOneField(CellCountInstance)
    dysplasia = models.CharField(max_length=50,
                                choices=ERYTHROPOIESIS_DYSPLASIA)
    comment = models.TextField(blank=True)

class GranulopoiesisFindings(models.Model):
    GRANULOPOIESIS_DYSPLASIA = (('None', 'None'),
                                ('Hypogranular', 'Hypogranular'),
                                ('Pelger', 'Pelger'),
                                ('Nuclear atypia', 'Nuclear atypia'),
                                ('Dohle bodies', 'Dohle bodies'))
    
    cell_count_instance = models.OneToOneField(CellCountInstance)
    dysplasia = models.CharField(max_length=50,
                                choices=GRANULOPOIESIS_DYSPLASIA)
    comment = models.TextField(blank=True)

class MegakaryocyteFeatures(models.Model):
    MEGAKARYOCYTE_RELATIVE_COUNT = (('Absent', 'Absent'),
                                    ('Reduced', 'Reduced'),
                                    ('Normal', 'Normal'),
                                    ('Increased', 'Increased'))
    MEGAKARYOCYTE_DYSPLASIA = (('None', 'None'),
                               ('Hypolobulated', 'Hypolobulated'),
                               ('Fragmented', 'Fragmented'))

    cell_count_instance = models.OneToOneField(CellCountInstance)
    relative_count = models.CharField(max_length=50,
                                choices=MEGAKARYOCYTE_RELATIVE_COUNT)
    dysplasia = models.CharField(max_length=50,
                                choices=MEGAKARYOCYTE_DYSPLASIA)
    comment = models.TextField(blank=True)

class IronStain(models.Model):
    ABSENT = 0
    GRADE_1 = 1
    GRADE_2 = 2
    GRADE_3 = 3
    GRADE_4 = 4
    IRON_STAIN_GRADE = ((ABSENT, 'Absent'),
                        (GRADE_1, 'Grade 1'),
                        (GRADE_2, 'Grade 2'),
                        (GRADE_3, 'Grade 3'),
                        (GRADE_4, 'Grade 4'))
    
    cell_count_instance = models.OneToOneField(CellCountInstance)
    stain_performed = models.BooleanField()
    iron_content = models.IntegerField(choices=IRON_STAIN_GRADE, blank=True, null=True)
    ringed_sideroblasts = models.NullBooleanField(blank=True, null=True)
    comment = models.TextField(blank=True)
