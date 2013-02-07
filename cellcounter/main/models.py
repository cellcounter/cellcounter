from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User

from colorful.fields import RGBColorField

class CellType(models.Model):
    readable_name = models.CharField(max_length=50)
    # TODO Use a slugfield
    machine_name = models.CharField(max_length=50, unique=True)
    abbr_name = models.CharField(max_length=10, unique=True)
    comment = models.TextField(blank=True)
    visualisation_colour = RGBColorField(blank=True)


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
