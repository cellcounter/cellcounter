import factory
from django.urls import reverse
from django_webtest import WebTest

from cellcounter.cc_kapi.factories import UserFactory
from cellcounter.main.models import *


CELLTYPE_LIST = [('Neutrophils', 'neutrophils'),
                 ('Metamyelocytes', 'meta'),
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

CELLTYPE_JSON = '[{"id":1,"readable_name":"Neutrophils","machine_name":"neutrophils","abbr_name":"neut","comment":"","visualisation_colour":"#4f6228"},{"id":2,"readable_name":"Metamyelocytes","machine_name":"meta","abbr_name":"meta","comment":"","visualisation_colour":"#77933c"},{"id":3,"readable_name":"Myelocytes","machine_name":"myelocytes","abbr_name":"myelo","comment":"","visualisation_colour":"#c3d69b"},{"id":4,"readable_name":"Promyelocytes","machine_name":"promyelocytes","abbr_name":"promyelo","comment":"","visualisation_colour":"#d7e4bd"},{"id":5,"readable_name":"Blasts","machine_name":"blasts","abbr_name":"blast","comment":"","visualisation_colour":"#ebf1de"},{"id":6,"readable_name":"Basophils","machine_name":"basophils","abbr_name":"baso","comment":"","visualisation_colour":"#8064a2"},{"id":7,"readable_name":"Eosinophils","machine_name":"eosinophils","abbr_name":"eo","comment":"","visualisation_colour":"#f79546"},{"id":8,"readable_name":"Erythroid","machine_name":"erythroid","abbr_name":"erythro","comment":"","visualisation_colour":"#ff0000"},{"id":9,"readable_name":"Lymphocytes","machine_name":"lymphocytes","abbr_name":"lympho","comment":"","visualisation_colour":"#ffffff"},{"id":10,"readable_name":"Monocytes","machine_name":"monocytes","abbr_name":"mono","comment":"","visualisation_colour":"#bfbfbf"},{"id":11,"readable_name":"Plasma cells","machine_name":"plasma_cells","abbr_name":"plasma","comment":"","visualisation_colour":"#0000ff"},{"id":12,"readable_name":"Other","machine_name":"other","abbr_name":"other","comment":"","visualisation_colour":"#f9ff00"},{"id":13,"readable_name":"Lymphoblasts","machine_name":"lymphoblasts","abbr_name":"ly_blasts","comment":"","visualisation_colour":"#606060"},{"id":14,"readable_name":"test","machine_name":"test","abbr_name":"test","comment":"Test","visualisation_colour":"#FFFFFF"}]'


class CellTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CellType

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
        self.assertEqual(CELLTYPE_JSON, response.body.decode("utf-8"))
