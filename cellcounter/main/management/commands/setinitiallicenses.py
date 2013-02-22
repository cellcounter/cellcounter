from django.core.management.base import BaseCommand, CommandError
from cellcounter.main.models import CellImage, CopyrightHolder, License
from django.contrib.auth.models import User
from optparse import make_option

class Command(BaseCommand):
    args = '<--uploader_pk=user_pk --license_pk=license_pk --copyright_pk=copyright_pk>'
    help = 'Sets initial uploader, licence and resource for all images.'
    option_list = ["--license_pk", "--copyright_pk", "--uploader_pk"]
    option_list = BaseCommand.option_list + (
        make_option('--uploader_pk',
                    help='Primary key of defualt user'),
        ) + (
        make_option('--copyright_pk',
                    help='Primary key of defualt copyright instance'),
        ) + (
        make_option('--license_pk',
                    help='Primary key of defualt licence instance'),
        )
    def handle(self, *args, **options):
        print args, options
        license = License.objects.get(pk = int(options["license_pk"]))
        copyright = CopyrightHolder.objects.get(pk = int(options["copyright_pk"]))
        print int(options["uploader_pk"])
        user = User.objects.get(pk = int(options["uploader_pk"]))
        print user
        for ci in CellImage.objects.all():
            try:
                ci.uploader
            except:
                ci.uploader = user
            try:
                ci.license
            except:
                ci.license = license
            try:
                ci.copyright
            except:
                ci.copyright = copyright
            ci.save() 
