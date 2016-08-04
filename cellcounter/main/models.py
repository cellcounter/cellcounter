import mimetypes
import os

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from django.db import models
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.encoding import python_2_unicode_compatible
from colorful.fields import RGBColorField
from PIL import Image


@python_2_unicode_compatible
class CellType(models.Model):
    readable_name = models.CharField(max_length=50)
    # TODO Use a slugfield
    machine_name = models.CharField(max_length=50, unique=True)
    abbr_name = models.CharField(max_length=10, unique=True)
    comment = models.TextField(blank=True)
    visualisation_colour = RGBColorField(blank=True)

    def __str__(self):
        return "CellType: {0}".format(self.readable_name)


@python_2_unicode_compatible
class CellImage(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    file = models.ImageField(upload_to="cell_images")
    thumbnail = models.ImageField(upload_to="cell_thumbnails", null=True, blank=True)
    celltype = models.ForeignKey(CellType)
    thumbnail_left = models.IntegerField()
    thumbnail_top = models.IntegerField()
    thumbnail_width = models.IntegerField()
    uploader = models.ForeignKey(User)
    copyright = models.ForeignKey('CopyrightHolder')
    license = models.ForeignKey('License')

    def __str__(self):
        return "CellImage: {0}".format(self.title)

    def similar_cells(self):
        groups = self.similarlookinggroup_set.all()
        similar_cells = []
        for group in groups:
            for image in group.cell_image.all():
                similar_cells.append(image)
        return similar_cells

    def generate_thumbnail(self):
        django_type = mimetypes.guess_type(self.file.file.name)[0]

        if django_type == 'image/jpeg':
            pil_type = 'jpeg'
            file_extension = 'jpg'
        elif django_type == 'image/png':
            pil_type = 'png'
            file_extension = 'png'

        image = Image.open(StringIO(self.file.read()))
        thumb_image = image.crop((self.thumbnail_left, self.thumbnail_top,
                                  self.thumbnail_left + self.thumbnail_width,
                                  self.thumbnail_top + self.thumbnail_width))
        thumb_image = thumb_image.resize((200, 200), Image.ANTIALIAS)
        temp_handle = StringIO()
        thumb_image.save(temp_handle, pil_type)
        temp_handle.seek(0)

        suf = SimpleUploadedFile(os.path.split(self.file.name)[-1],
                                 temp_handle.read(), content_type=django_type)
        self.thumbnail.save(
            '%s_thumbnail.%s' % (os.path.splitext(suf.name)[0], file_extension),
            suf)


@python_2_unicode_compatible
class SimilarLookingGroup(models.Model):
    name = models.CharField(max_length=100)
    cell_image = models.ManyToManyField("CellImage")

    def __str__(self):
        return "CellGroup: {0}".format(self.name)


@python_2_unicode_compatible
class License(models.Model):
    title = models.CharField(max_length=100)
    details = models.TextField()

    def __str__(self):
        return "License: {0}".format(self.title)


@python_2_unicode_compatible
class CopyrightHolder(models.Model):
    name = models.CharField(max_length=300)
    link_title = models.CharField(max_length=300, null=True, blank=True)
    link_url = models.CharField(max_length=300, null=True, blank=True)
    user = models.ManyToManyField(User)  # These users may apply this copyright to an image

    def __str__(self):
        return "CopyrightHolder: {0}".format(self.name)
