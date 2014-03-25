import datetime
import factory

from django.contrib.auth.models import User
from django.utils.timezone import utc
from django.core.urlresolvers import reverse
from django_webtest import WebTest

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
                 ('Lymphoblasts', 'ly_blasts'),
                 ('Other', 'other')]

CELLTYPE_LIST = '[{"id": 1, "readable_name": "test", "machine_name": "test", "abbr_name": "test", "comment": "Test", "visualisation_colour": "#FFFFFF"}]'


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
    
    readable_name = 'test'
    machine_name = 'test'
    abbr_name = 'test'
    comment = "Test"
    visualisation_colour = '#FFFFFF'


class TestMainViews(WebTest):
    def setUp(self):
        self.user = UserFactory()
        self.cell_type = CellTypeFactory()

    def test_new_count_view(self):
        response = self.app.get(reverse('new_count'))
        self.assertFalse(response.context['logged_in'])
        self.assertEqual(200, response.status_code)

    def test_new_count_login(self):
        response = self.app.get(reverse('new_count'), user=self.user)
        self.assertTrue(response.context['logged_in'])
        self.assertEqual(200, response.status_code)

    def test_get_celltype_api(self):
        response = self.app.get(reverse('cell_types'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(CELLTYPE_LIST, response.body)