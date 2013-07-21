import datetime
import factory

from django.contrib.auth.models import User
from django.utils.timezone import utc

from cellcounter.main.models import *

CELLTYPE_LIST = [('Neutrophils', 'neutrophils'),
                 ('Band Forms', 'band_forms'),
                 ('Myelocytes', 'myelocytes'),
                 ('Promyelocytes', 'promyelocytes'),
                 ('Blasts', 'blasts'),
                 ('Basophils', 'basophils'),
                 ('Eosinophils', 'eosinophils'),
                 ('Erythroid', 'erythroid'),
                 ('Lymphocytes', 'lymphocytes'),
                 ('Monocytes', 'monocytes'),
                 ('Plasma cells', 'plasma_cells'),
                 ('Other', 'other'),]

class UserFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = User

    username = factory.Sequence(lambda n: "test%s" % n)
    first_name = factory.Sequence(lambda n: "test%s" % n)
    last_name = factory.Sequence(lambda n: "test%s" % n)
    email = factory.Sequence(lambda n: "test%s@example.com" % n)
    password = 'pbkdf2_sha256$10000$8na6FeT9qxUY$2LUHCd+ipsMynWF0RTz+vdDQ0GDS1ZS+Isi5k3dyi3A='
    is_staff = False
    is_active = True
    is_superuser = False
    last_login = datetime.datetime.utcnow().replace(tzinfo=utc)
    date_joined = datetime.datetime.utcnow().replace(tzinfo=utc)

class CellTypeFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = CellType
    
    readable_name = '' 
    machine_name = '' 
    abbr_name = ''
    comment = ""
    visualisaion_colour = ''