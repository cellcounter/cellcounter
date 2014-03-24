from django.db import models
from django.contrib.auth.models import User

from colorful.fields import RGBColorField


class CellType(models.Model):
    readable_name = models.CharField(max_length=50)
    # TODO Use a slugfield
    machine_name = models.CharField(max_length=50, unique=True)
    abbr_name = models.CharField(max_length=10, unique=True)
    comment = models.TextField(blank=True)
    visualisation_colour = RGBColorField(blank=True)
    
    def __unicode__(self):
        return self.readable_name


class CellImage(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    file = models.ImageField(upload_to="cell_images")
    celltype = models.ForeignKey(CellType)
    thumbnail_left = models.IntegerField()
    thumbnail_top = models.IntegerField()
    thumbnail_width = models.IntegerField()
    uploader = models.ForeignKey(User)
    copyright = models.ForeignKey('CopyrightHolder')
    license = models.ForeignKey('License')

    def similar_cells(self):
        groups = self.similarlookinggroup_set.all()
        similar_cells = []
        for group in groups:
            for image in group.cell_image.all():
                similar_cells.append(image)
        return similar_cells

    def __unicode__(self):
        return self.title


class SimilarLookingGroup(models.Model):
    name = models.CharField(max_length=100)
    cell_image = models.ManyToManyField("CellImage")

    def __unicode__(self):
        return self.name


class License(models.Model):
    title = models.CharField(max_length=100)
    details = models.TextField()

    def __unicode__(self):
        return self.title


class CopyrightHolder(models.Model):
    name = models.CharField(max_length=300)
    link_title = models.CharField(max_length=300, null=True, blank=True)
    link_url = models.CharField(max_length=300, null=True, blank=True)
    user = models.ManyToManyField(User)  # These users may apply this copyright to an image

    def __unicode__(self):
        return self.name
