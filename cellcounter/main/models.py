from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User

from colorful.fields import RGBColorField

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
    # TODO Use a slugfield
    machine_name = models.CharField(max_length=50, unique=True)
    abbr_name = models.CharField(max_length=10, unique=True)
    comment = models.TextField(blank=True)
    visualisation_colour = RGBColorField(blank=True)

    def __unicode__(self):
        return self.readable_name

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
    cell_count_instance = models.OneToOneField(CellCountInstance)
    no_dysplasia = models.BooleanField(default=True)
    nuclear_asynchrony = models.BooleanField(default=False)
    multinucleated_forms = models.BooleanField(default=False)
    ragged_haemoglobinisation = models.BooleanField(default=False)
    megaloblastic_change = models.BooleanField(default=False)
    comment = models.TextField(blank=True)

    def get_dysplasia(self):
        if self.no_dysplasia:
            return None
        else:
            return [x[0] for x in [('Nuclear asynchrony', self.nuclear_asynchrony),
                                   ('Multinucleated forms', self.multinucleated_forms),
                                   ('Ragged haemoglobinisation', self.ragged_haemoglobinisation),
                                   ('Megaloblastic change', self.megaloblastic_change)]
                                   if x[1]]

class GranulopoiesisFindings(models.Model):
    cell_count_instance = models.OneToOneField(CellCountInstance)
    no_dysplasia = models.BooleanField(default=True)
    hypogranular = models.BooleanField(default=False)
    pelger = models.BooleanField(default=False)
    nuclear_atypia = models.BooleanField(default=False)
    dohle_bodies = models.BooleanField(default=False)
    comment = models.TextField(blank=True)

    def get_dysplasia(self):
        if self.no_dysplasia:
            return None
        else:
            return [x[0] for x in [('Hypogranular', self.hypogranular),
                                   ('Pelger', self.pelger),
                                   ('Nuclear atypia', self.nuclear_atypia),
                                   ('Dohle bodies', self.dohle_bodies)]
                                   if x[1]]

class MegakaryocyteFeatures(models.Model):
    MEGAKARYOCYTE_RELATIVE_COUNT = (('Absent', 'Absent'),
                                    ('Reduced', 'Reduced'),
                                    ('Normal', 'Normal'),
                                    ('Increased', 'Increased'))
    cell_count_instance = models.OneToOneField(CellCountInstance)
    relative_count = models.CharField(max_length=50,
                                choices=MEGAKARYOCYTE_RELATIVE_COUNT)
    no_dysplasia = models.BooleanField(default=True)
    hypolobulated = models.BooleanField(default=False)
    fragmented = models.BooleanField(default=False)
    micromegakaryocytes = models.BooleanField(default=False)
    comment = models.TextField(blank=True)

    def get_dysplasia(self):
        if self.no_dysplasia:
            return None
        else:
            return [x[0] for x in [('Hypolobulated', self.hypolobulated),
                                   ('Fragmented', self.fragmented),
                                   ('Micromegakaryocytes', self.micromegakaryocytes)]
                                   if x[1]]

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

class CellImage(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    file  = models.ImageField(upload_to= "cell_images")
    celltype = models.ForeignKey(CellType)
    thumbnail_left = models.IntegerField()
    thumbnail_top = models.IntegerField()
    thumbnail_width = models.IntegerField()
    def similar_cells(self):
        groups = self.similarlookinggroup_set.all()
        similarcells = []
        for group in groups:
            for image in group.cell_image.all():
                similarcells.append(image)
        return similarcells
    def __unicode__(self):
        return self.title

class SimilarLookingGroup(models.Model):
    name = models.CharField(max_length=100)
    cell_image = models.ManyToManyField("CellImage")    
    def __unicode__(self):
        return self.name
