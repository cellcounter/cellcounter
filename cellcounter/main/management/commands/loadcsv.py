from django.core.management.base import BaseCommand, CommandError
from cellcounter.main.models import CellImage, SimilarLookingGroup, CellType
import csv

class dialect(csv.Dialect):
    pass

class Command(BaseCommand):
    args = '<csvfile1 csvfile2 ...>'
    help = 'Loads images and descriptions from specified csv file(s)'

    def handle(self, *args, **options):
         for filename in args:
             file_ = csv.DictReader(open(filename), dialect="excel-tab")
             for line in file_:
                 try:
                     celltype = CellType.objects.get(readable_name = line["CellType"])
                 except:
                     print "Cell Type not found:" + line["CellType"]
                 ci = CellImage(title = line["Title"],
                                description = line["Description"],
                                file = line["Filename"],
                                celltype = celltype)
                 ci.save() 
