import re
import datetime

import factory
import webtest
from django.test import TestCase
from django.test.client import Client
from django.utils.timezone import utc
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django_webtest import WebTest

from cellcounter.main.models import *

CELLTYPE_LIST = [('Neutrophils', 'neut'),
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

class UserFactory(factory.Factory):
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

class CellTypeFactory(factory.Factory):
    FACTORY_FOR = CellType
    
    readable_name = '' 
    machine_name = '' 
    comment = ""

class CellCountInstanceFactory(factory.Factory):
    FACTORY_FOR = CellCountInstance

    user = factory.SubFactory(UserFactory)
    datetime_submitted = datetime.datetime.utcnow().replace(tzinfo=utc)
    datetime_updated = datetime.datetime.utcnow().replace(tzinfo=utc)
    tissue_type = 'Bone marrow'
    overall_comment = ''

class CellCountFactory(factory.Factory):
    FACTORY_FOR = CellCount

    cell_count_instance = factory.SubFactory(CellCountInstanceFactory)
    normal_count = 5
    abnormal_count = 5
    comment = ''

class BoneMarrowBackgroundFactory(factory.Factory):
    FACTORY_FOR = BoneMarrowBackground

    cell_count_instance = factory.SubFactory(CellCountInstanceFactory)
    trail_cellularity = 'Hypo'
    particle_cellularity = 'Hypo'
    particulate = 'No particles'
    haemodilution = 'Mild'
    site = 'Iliac Crest'
    ease_of_aspiration = 'Easy'

class ErythropoiesisFindingsFactory(factory.Factory):
    FACTORY_FOR = ErythropoiesisFindings

    cell_count_instance = factory.SubFactory(CellCountInstanceFactory)
    no_dysplasia = True
    nuclear_asynchrony = False
    multinucleated_forms = False
    ragged_haemoglobinisation = False
    megaloblastic_change = False
    comment = ''

class GranulopoiesisFindingsFactory(factory.Factory):
    FACTORY_FOR = GranulopoiesisFindings

    cell_count_instance = factory.SubFactory(CellCountInstanceFactory)
    no_dysplasia = True
    hypogranular = False
    pelger = False
    nuclear_atypia = False
    dohle_bodies = False
    comment = ''

class MegakaryocyteFeaturesFactory(factory.Factory):
    FACTORY_FOR = MegakaryocyteFeatures

    cell_count_instance = factory.SubFactory(CellCountInstanceFactory)
    relative_count = 'Reduced'
    no_dysplasia = True
    hypolobulated = False
    fragmented = False
    micromegakaryocytes = False
    comment = ''

class IronStainFactory(factory.Factory):
    FACTORY_FOR = IronStain

    cell_count_instance = factory.SubFactory(CellCountInstanceFactory)
    stain_performed = False
    comment = ''

class CellCountInstanceRelatedFactory(CellCountInstanceFactory):
    """Creates a CellCountInstanceFactory, but then adds in generation for
    related objects required for Report view generation."""
    bm_background = factory.RelatedFactory(BoneMarrowBackgroundFactory, 
                                           'cell_count_instance')
    erythropoiesis_findings = factory.RelatedFactory(
            ErythropoiesisFindingsFactory, 'cell_count_instance')
    granulopoiesis_findings = factory.RelatedFactory(
            GranulopoiesisFindingsFactory, 'cell_count_instance')
    megakaryocyte_features = factory.RelatedFactory(
            MegakaryocyteFeaturesFactory, 'cell_count_instance')
    ironstain = factory.RelatedFactory(IronStainFactory,
                                       'cell_count_instance')

class CellCountInstanceTestCase(TestCase):

    def setUp(self):
        self.cellcount_instance = CellCountInstanceFactory()
        for cell in CellType.objects.all():
            cellcount = CellCountFactory(
                    cell_count_instance=self.cellcount_instance, cell=cell)

    def test_me_ratio(self):
        self.assertEquals(
                self.cellcount_instance.myeloid_erythroid_ratio(), 7.0)

    def test_me_ratio_erythroid_0(self):
        cellcount_instance_2 = CellCountInstanceFactory()
        for cell in CellType.objects.exclude(machine_name='erythroid'):
            cellcount = CellCountFactory(
                    cell_count_instance=self.cellcount_instance, cell=cell)
        cell = CellType.objects.get(machine_name='erythroid')
        cellcount = CellCountFactory(cell_count_instance=cellcount_instance_2, 
                cell=cell, normal_count=0, abnormal_count=0)
        self.assertEquals(cellcount_instance_2.myeloid_erythroid_ratio(), 
                'Unable to calculate, erythroid count = 0')

    def test_total_cellcount(self):
        self.assertEquals(self.cellcount_instance.total_cellcount(), 120)

    def test_myeloid_cellcount(self):
        self.assertEquals(self.cellcount_instance.myeloid_cellcount(), 70)

    def test_erythroid_cellcount(self):
        self.assertEquals(self.cellcount_instance.erythroid_cellcount(), 10)

class CellCountTestCase(TestCase):

    def test_total_count(self):
        cell = CellCountFactory.build()
        self.assertEquals(cell.get_total_count(), 10)

    def test_percentage_count(self):
        cellcount_instance = CellCountInstanceFactory()
        for cell in CellType.objects.all():
            cellcount = CellCountFactory(
                    cell_count_instance=cellcount_instance, cell=cell)
        self.assertEquals(cellcount.percentage(), 8.0)

class TestSubmitCount(WebTest):

    def setUp(self):
        self.cellcount_instance = CellCountInstanceFactory(user__username='foo')
        for cell in CellType.objects.all():
            cellcount = CellCountFactory(
                    cell_count_instance=self.cellcount_instance, cell=cell)

    def test_logged_out_302(self):
        response = self.app.get(reverse('new_count'))
        self.assertRedirects(response, "%s?next=%s" %(reverse('login'),
                             reverse('new_count')))

    def test_logged_in_get(self):
        form = self.app.get(reverse('new_count'), user='foo').form
        # Cellcount main details
        self.assertIn('cellcount-tissue_type', form.fields)

        # Bonemarrow stats
        self.assertIn('bonemarrow-trail_cellularity', form.fields)
        self.assertIn('bonemarrow-particle_cellularity', form.fields)
        self.assertIn('bonemarrow-particulate', form.fields)
        self.assertIn('bonemarrow-haemodilution', form.fields)
        self.assertIn('bonemarrow-site', form.fields)
        self.assertIn('bonemarrow-ease_of_aspiration', form.fields)

        # Granulopoiesis
        self.assertIn('granulopoiesis-no_dysplasia', form.fields)
        self.assertIn('granulopoiesis-hypogranular', form.fields)
        self.assertIn('granulopoiesis-pelger', form.fields)
        self.assertIn('granulopoiesis-nuclear_atypia', form.fields)
        self.assertIn('granulopoiesis-dohle_bodies', form.fields)
        self.assertIn('granulopoiesis-comment', form.fields)

        # Erythroipoiesis
        self.assertIn('erythropoiesis-no_dysplasia', form.fields)
        self.assertIn('erythropoiesis-nuclear_asynchrony', form.fields)
        self.assertIn('erythropoiesis-multinucleated_forms', form.fields)
        self.assertIn('erythropoiesis-ragged_haemoglobinisation', form.fields)
        self.assertIn('erythropoiesis-megaloblastic_change', form.fields)
        self.assertIn('erythropoiesis-comment', form.fields)

        # Megakaryocytes
        self.assertIn('megakaryocyte-relative_count', form.fields)
        self.assertIn('megakaryocyte-no_dysplasia', form.fields)
        self.assertIn('megakaryocyte-hypolobulated', form.fields)
        self.assertIn('megakaryocyte-fragmented', form.fields)
        self.assertIn('megakaryocyte-micromegakaryocytes', form.fields)
        self.assertIn('megakaryocyte-comment', form.fields)

        # Iron stain
        self.assertIn('ironstain-stain_performed', form.fields)
        self.assertIn('ironstain-ringed_sideroblasts', form.fields)
        self.assertIn('ironstain-iron_content', form.fields)
        self.assertIn('ironstain-comment', form.fields)

        # Overall comment
        self.assertIn('cellcount-overall_comment', form.fields)

        # For all cells
        for celltype in CELLTYPE_LIST:
            self.assertIn(celltype[1]+'-cell', form.fields)
            self.assertIn(celltype[1]+'-normal_count', form.fields)
            self.assertIn(celltype[1]+'-abnormal_count', form.fields)

    def test_logged_in_post_valid(self):
        form = self.app.get(reverse('new_count'), user='foo').form
        form.set('cellcount-tissue_type', 'Bone marrow')
        form.set('bonemarrow-trail_cellularity', 'Normal')
        form.set('bonemarrow-particle_cellularity', 'Normal')
        form.set('bonemarrow-particulate', 'No particles')
        form.set('bonemarrow-haemodilution', 'Moderate')
        form.set('bonemarrow-site', 'Iliac Crest')
        form.set('bonemarrow-ease_of_aspiration', 'Easy')
        form.set('granulopoiesis-no_dysplasia', True)
        form.set('erythropoiesis-no_dysplasia', True)
        form.set('megakaryocyte-relative_count', 'Normal')
        form.set('megakaryocyte-no_dysplasia', True)
        form.set('ironstain-stain_performed', False)
        form.set('cellcount-overall_comment', 'Unremarkable aspiration')

        response = form.submit().follow()
        self.assertIn('Count submitted successfully', response.body)
        cell_count = CellCountInstance.objects.get(id=2)
        self.assertEqual('Unremarkable aspiration', cell_count.overall_comment)

    def test_invalid_form(self):
        # Missing bonemarrow-site
        form = self.app.get(reverse('new_count'), user='foo').form
        form.set('cellcount-tissue_type', 'Bone marrow')
        form.set('bonemarrow-trail_cellularity', 'Normal')
        form.set('bonemarrow-particle_cellularity', 'Normal')
        form.set('bonemarrow-particulate', 'No particles')
        form.set('bonemarrow-haemodilution', 'Moderate')
        form.set('bonemarrow-ease_of_aspiration', 'Easy')
        form.set('megakaryocyte-relative_count', 'Normal')
        form.set('cellcount-overall_comment', 'Unremarkable aspiration')

        response = form.submit()
        self.assertNotIn('Count submitted successfully', response.body)

class TestViewCount(WebTest):
    def setUp(self):
        self.cellcount_instance = CellCountInstanceRelatedFactory(
                user__username='foo')
        for cell in CellType.objects.all():
            cellcount = CellCountFactory(
                    cell_count_instance=self.cellcount_instance, cell=cell)

        cellcount_instance = CellCountInstanceRelatedFactory()
        for cell in CellType.objects.all():
            cellcount = CellCountFactory(
                    cell_count_instance=cellcount_instance, cell=cell)

    def test_existent_loggedout(self):
        response = self.app.get(reverse('view_count', kwargs={'count_id': 1}))
        self.assertRedirects(response,
                             "%s?next=%s" %(reverse('login'),
                             reverse('view_count', kwargs={'count_id': 1})))

    def test_nonexistent_loggedout(self):
        response = self.app.get(reverse('view_count', kwargs={'count_id': 25}))
        self.assertRedirects(response,
                             "%s?next=%s" %(reverse('login'),
                             reverse('view_count', kwargs={'count_id': 25})))

    def test_nonexistent_count(self):
        response = self.app.get(reverse('view_count', kwargs={'count_id': 25}),
                                user='foo', status=404)
        self.assertEquals('404 NOT FOUND', response.status)

    def test_view_user_count(self):
        response = self.app.get(reverse('view_count', kwargs={'count_id': 1}),
                                user='foo')
        self.assertEquals('200 OK', response.status)
        self.assertEqual(response.html.find("h1", text=re.compile("Report")),
                         "Report")

    def test_view_nonuser_count(self):
        response = self.app.get(reverse('view_count', kwargs={'count_id': 2}),
                                user='foo', status=403)
        self.assertEqual('403 FORBIDDEN', response.status)

class TestViewCountsList(WebTest):
    def setUp(self):
        self.cellcount_instance = CellCountInstanceRelatedFactory(user__username='foo')
        for cell in CellType.objects.all():
            cellcount = CellCountFactory(
                    cell_count_instance=self.cellcount_instance, cell=cell)

    def test_view_my_count_loggedout(self):
        response = self.app.get(reverse('my_counts', kwargs={'pk': 1}))
        self.assertRedirects(response,
                "%s?next=%s" %(reverse('login'),
                    reverse('my_counts', kwargs={'pk':1})))

    def test_view_my_count_loggedin(self):
        response = self.app.get(reverse('my_counts', kwargs={'pk': 1}), 
                                user='foo')
        self.assertEqual('200 OK', response.status)
        self.assertEqual(response.html.find("h2", text=re.compile("My Counts")),
                         "My Counts")
        self.assertEqual(response.html.find("b", text=re.compile("Count ID #1")),
                         "Count ID #1")
        self.assertTrue(response.html.find("a", href=re.compile("count/1/")))
        self.assertTrue(response.html.find("a", 
                        href=re.compile("count/1/edit/")))
        self.assertTrue(response.html.find("a", 
                        href=re.compile("count/1/delete/")))
        self.assertTrue(response.html.find("a", 
                        href=re.compile("count/new/")))

class TestEditCount(WebTest):
    def setUp(self):
        self.cellcount_instance = CellCountInstanceRelatedFactory(user__username='foo')
        for cell in CellType.objects.all():
            cellcount = CellCountFactory(
                    cell_count_instance=self.cellcount_instance, cell=cell)
        cellcount_instance = CellCountInstanceRelatedFactory()
        for cell in CellType.objects.all():
            cellcount = CellCountFactory(
                    cell_count_instance=cellcount_instance, cell=cell)

    def test_edit_nonexistent_lo(self):
        response = self.app.get(reverse('edit_count', kwargs={'count_id': 25}))
        self.assertRedirects(response,
                             "%s?next=%s" %(reverse('login'),
                             reverse('edit_count', kwargs={'count_id': 25})))

    def test_edit_nonexistent_li(self):
        response = self.app.get(reverse('edit_count', kwargs={'count_id': 25}),
                                user='foo', status=404)
        self.assertEquals('404 NOT FOUND', response.status)

    def test_edit_own_li(self):
        form = self.app.get(reverse('edit_count', kwargs={'count_id': 1}),
                                user='foo').form
        self.assertIn('cellcount-tissue_type', form.fields)

        # Bonemarrow stats
        self.assertIn('bonemarrow-trail_cellularity', form.fields)
        self.assertIn('bonemarrow-particle_cellularity', form.fields)
        self.assertIn('bonemarrow-particulate', form.fields)
        self.assertIn('bonemarrow-haemodilution', form.fields)
        self.assertIn('bonemarrow-site', form.fields)
        self.assertIn('bonemarrow-ease_of_aspiration', form.fields)

        # Granulopoiesis
        self.assertIn('granulopoiesis-no_dysplasia', form.fields)
        self.assertIn('granulopoiesis-hypogranular', form.fields)
        self.assertIn('granulopoiesis-pelger', form.fields)
        self.assertIn('granulopoiesis-nuclear_atypia', form.fields)
        self.assertIn('granulopoiesis-dohle_bodies', form.fields)
        self.assertIn('granulopoiesis-comment', form.fields)

        # Erythroipoiesis
        self.assertIn('erythropoiesis-no_dysplasia', form.fields)
        self.assertIn('erythropoiesis-nuclear_asynchrony', form.fields)
        self.assertIn('erythropoiesis-multinucleated_forms', form.fields)
        self.assertIn('erythropoiesis-ragged_haemoglobinisation', form.fields)
        self.assertIn('erythropoiesis-megaloblastic_change', form.fields)
        self.assertIn('erythropoiesis-comment', form.fields)

        # Megakaryocytes
        self.assertIn('megakaryocyte-relative_count', form.fields)
        self.assertIn('megakaryocyte-no_dysplasia', form.fields)
        self.assertIn('megakaryocyte-hypolobulated', form.fields)
        self.assertIn('megakaryocyte-fragmented', form.fields)
        self.assertIn('megakaryocyte-micromegakaryocytes', form.fields)
        self.assertIn('megakaryocyte-comment', form.fields)

        # Iron stain
        self.assertIn('ironstain-stain_performed', form.fields)
        self.assertIn('ironstain-ringed_sideroblasts', form.fields)
        self.assertIn('ironstain-iron_content', form.fields)
        self.assertIn('ironstain-comment', form.fields)

        # Overall comment
        self.assertIn('cellcount-overall_comment', form.fields)

    def test_post_edit_own(self):
        form = self.app.get(reverse('edit_count', kwargs={'count_id': 1}),
                                user='foo').form
        form.set('cellcount-overall_comment', 'Exciting aspiration')

        response = form.submit().follow()
        self.assertIn('Count edited successfully', response.body)
        cell_count = CellCountInstance.objects.get(id=1)
        self.assertEqual('Exciting aspiration', cell_count.overall_comment)

    def test_edit_others_li(self):
        response = self.app.get(reverse('edit_count', kwargs={'count_id': 2}),
                                user='foo', status=403)
        self.assertEqual('403 FORBIDDEN', response.status)
