from django.test import TestCase
from django.contrib.auth.models import User
from django.core.cache import cache

from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate

from .views import ListCreateCountInstanceAPI

factory = APIRequestFactory()
view = ListCreateCountInstanceAPI.as_view()


class TestCountInstanceAPI(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('basic', 'basic@example.com', 'basic')
        self.staff_user = User.objects.create_superuser('permitted',
                                                        'permitted@example.com',
                                                        'password')
        cache.clear()

    def test_create_permissions(self):
        request = factory.post('/', {'count_total': 100}, format='json')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        request = factory.post('/', {'count_total': 100}, format='json')
        force_authenticate(request, user=self.staff_user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        request = factory.post('/', {'count_total': 100}, format='json')
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
        for dummy in range(2):
            response = view(request)
        self.assertEqual(429, response.status_code)
