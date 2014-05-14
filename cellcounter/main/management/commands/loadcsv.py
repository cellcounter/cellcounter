import csv
from django.core.management.base import BaseCommand
from cellcounter.main.models import CellImage, CellType


class Command(BaseCommand):
    args = '<csvfile1 csvfile2 ...>'
    help = 'Loads images and descriptions from specified csv file(s)'

    def handle(self, *args, **options):
        for filename in args:
            file_ = csv.DictReader(open(filename), dialect="excel-tab")
            for line in file_:
                try:
                    celltype = CellType.objects.get(readable_name=line["CellType"])
                except CellType.DoesNotExist:
                    print "Cell Type not found:" + line["CellType"]
                ci = CellImage(title=line["Title"],
                               description=line["Description"],
                               file=line["Filename"],
                               thumbnail_left=line["X"],
                               thumbnail_top=line["Y"],
                               thumbnail_width=line["Pixels"],
                               celltype=celltype)
                ci.save()
