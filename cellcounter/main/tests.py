from django.core.urlresolvers import reverse
from django_webtest import WebTest
from rest_framework.renderers import JSONRenderer

from cellcounter.main.factories import UserFactory, CellTypeFactory
from cellcounter.main.models import CellType
from cellcounter.main.serializers import CellTypeSerializer

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
        queryset = CellType.objects.all().order_by('id')
        serializer = CellTypeSerializer(queryset, many=True)
        self.assertEqual(200, response.status_code)
        self.assertEqual(JSONRenderer().render(serializer.data), response.body)
