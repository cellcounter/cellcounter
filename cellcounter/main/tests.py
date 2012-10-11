from django.test import TestCase
from django.contrib.auth.models import User
from django.test.client import Client

from django.core.urlresolvers import reverse

from cellcounter.main.models import CellCountInstance
from cellcounter.main.utils import POST_DATA

class TestSubmitPageContext(TestCase):
    fixtures = ['test_user.json', 'test_count.json']

    def test_get_submit_page_loggedout(self):
        client = Client()
        response = client.get(reverse('new_count'), follow=True)
        self.assertRedirects(response, 'http://testserver/login/?next=/count/new/')

    def test_get_submit_page_loggedin(self):
        client = Client()
        client.login(username='test', password='test')
        response = client.get(reverse('new_count'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/submit.html')
        self.assertIn('cellcount', response.context)
        self.assertIn('bonemarrowbackground', response.context)
        self.assertIn('erythropoiesis_form', response.context)
        self.assertIn('granulopoiesis_form', response.context)
        self.assertIn('megakaryocyte_form', response.context)
        self.assertIn('cellcountformslist', response.context)

    def test_post_submit_page(self):
        client = Client()
        client.login(username='test', password='test')
        response = client.post(reverse('new_count'), POST_DATA)

        self.assertRedirects(response, 'http://testserver/')

class TestViewCount(TestCase):

    fixtures = ['test_user.json', 'test_count.json']

    def test_view_nonexistent_page_loggedin(self):
        client = Client()
        client.login(username='test', password='test')
        response = client.get(reverse('view_count', kwargs={'count_id': 25}))
        self.assertEqual(response.status_code, 404)
    
    def test_view_nonexistent_page_loggedout(self):
        client = Client()
        response = client.get(reverse('view_count', kwargs={'count_id': 25}), follow=True)
        self.assertRedirects(response, 'http://testserver/login/?next=/count/25/')

    def test_view_existing_page_loggedin(self):
        client = Client()
        client.login(username='test', password='test')
        response = client.get(reverse('view_count', kwargs={'count_id': 1}))
        self.assertEqual(response.status_code, 200)
    
    def test_view_existing_page_loggedout(self):
        client = Client()
        response = client.get(reverse('view_count', kwargs={'count_id': 1}), follow=True)
        self.assertRedirects(response, 'http://testserver/login/?next=/count/1/')

    def test_view_own_page(self):
        client = Client()
        client.login(username='test', password='test')
        response = client.get(reverse('view_count', kwargs={'count_id': 1}))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/report.html')
        self.assertIn('cellcount', response.context)
        self.assertIn('bonemarrowbackground', response.context)
        self.assertIn('erythropoiesis', response.context)
        self.assertIn('granulopoiesis', response.context)
        self.assertIn('megakaryocytes', response.context)
        self.assertIn('cellcount_list', response.context)

    def test_view_other_page(self):
        client = Client()
        client.login(username='test', password='test')
        response = client.get(reverse('view_count', kwargs={'count_id': 2}))
        self.assertEqual(response.status_code, 403)
