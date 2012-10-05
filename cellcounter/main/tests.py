from django.test import TestCase
from django.test.client import Client

from django.core.urlresolvers import reverse

class TestSubmitPageContext(TestCase):

    def setUp(self):
        self.client = Client()

    def test_get_submit_page_context(self):
        response = self.client.get(reverse('new_count'))

        # Assert page responds 200 and with correct template
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/submit.html')

        # Assert we have the requisite forms in context
        self.assertIn('cellcount', response.context)
        self.assertIn('bonemarrowbackground', response.context)
        self.assertIn('erythropoiesis_form', response.context)
        self.assertIn('granulopoiesis_form', response.context)
        self.assertIn('megakaryocyte_form', response.context)
