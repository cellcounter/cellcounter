from importlib import import_module

from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.core.cache import cache
from django.test import TestCase, RequestFactory

from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate

from .views import ListCreateCountInstanceAPI
from .middleware import StatsSessionMiddleware
from .models import CountInstance

factory = APIRequestFactory()
view = ListCreateCountInstanceAPI.as_view()


class TestStatsMiddleware(TestCase):
    def setUp(self):
        self.request = RequestFactory().get(reverse('create-count-instance'))
        self.request.session = {}
        self.request.COOKIES = {}
        self.mw = StatsSessionMiddleware()

    def test_empty_session(self):
        self.mw.process_request(self.request)
        self.assertIsNotNone(self.request.session.session_key)

    def test_no_key_session(self):
        self.mw.process_request(self.request)
        self.assertIsNotNone(self.request.session.session_key)

    def test_key_session(self):
        """Don't create new session id when one is already set
        """
        session_engine = import_module(settings.SESSION_ENGINE)
        SessionStore = session_engine.SessionStore
        session_id = SessionStore(None)
        session_id.save()
        self.request.COOKIES['sessionid'] = session_id.session_key
        self.mw.process_request(self.request)
        self.assertEqual(session_id.session_key, self.request.session.session_key)


class TestCountInstanceAPI(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('basic', 'basic@example.com', 'basic')
        self.staff_user = User.objects.create_superuser('permitted',
                                                        'permitted@example.com',
                                                        'password')
        self.url = reverse('create-count-instance')
        self.data = {'count_total': 100}
        cache.clear()

    def test_create_permissions(self):
        request = factory.post('/', {'count_total': 100}, format='json')
        StatsSessionMiddleware().process_request(request)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        request = factory.post('/', {'count_total': 100}, format='json')
        StatsSessionMiddleware().process_request(request)
        force_authenticate(request, user=self.staff_user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        request = factory.post('/', {'count_total': 100}, format='json')
        StatsSessionMiddleware().process_request(request)
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_safe_permissions(self):
        request = factory.get('/')
        force_authenticate(request, user=self.staff_user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        request = factory.head('/')
        force_authenticate(request, user=self.staff_user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        request = factory.options('/')
        force_authenticate(request, user=self.staff_user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anonymous_permissions(self):
        request = factory.get('/')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        request = factory.head('/')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        request = factory.options('/')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_ratelimit_exceeded(self):
        request = factory.post('/', {'count_total': 100}, format='json')
        StatsSessionMiddleware().process_request(request)
        for dummy in range(2):
            response = view(request)
        self.assertEqual(429, response.status_code)
