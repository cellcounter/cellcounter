from django.core.urlresolvers import reverse
from django.test import TestCase
from django_webtest import WebTest
from rest_framework.renderers import JSONRenderer

from cellcounter.main import models, factories
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


class TestModelStrings(TestCase):
    def test_celltype(self):
        celltype = factories.CellTypeFactory()
        self.assertEqual(str(celltype), "CellType: {0}".format(celltype.readable_name))

    def test_cellimage(self):
        image = factories.CellImageFactory()
        self.assertEqual(str(image), "CellImage: {0}".format(image.title))

    def test_similar_looking_group(self):
        group = factories.SimilarLookingGroupFactory()
        self.assertEqual(str(group), "CellGroup: {0}".format(group.name))

    def test_license(self):
        image_license = factories.LicenseFactory()
        self.assertEqual(str(image_license), "License: {0}".format(image_license.title))

    def test_copyright_holder(self):
        copyright_holder = factories.CopyrightHolderFactory()
        self.assertEqual(str(copyright_holder), "CopyrightHolder: {0}".format(copyright_holder.name))


class TestMainViews(WebTest):
    def setUp(self):
        self.user = factories.UserFactory()
        self.cell_type = factories.CellTypeFactory()

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
        queryset = models.CellType.objects.all().order_by('id')
        serializer = CellTypeSerializer(queryset, many=True)
        self.assertEqual(200, response.status_code)
        self.assertEqual(JSONRenderer().render(serializer.data), response.body)
