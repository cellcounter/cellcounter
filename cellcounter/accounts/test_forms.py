from urllib.parse import urlparse

import re
from django.contrib.auth.tokens import default_token_generator
from django.core import mail
from django.urls import reverse
from django.test import TestCase
from django.test.client import RequestFactory
from django.utils.http import urlsafe_base64_decode

from cellcounter.cc_kapi.factories import UserFactory
from .forms import EmailUserCreationForm, PasswordResetForm


class TestEmailUserCreationForm(TestCase):
    def test_valid(self):
        data = {'username': 'joebloggs', 'email': 'joe@example.org', 'password1': 'new_pwd', 'password2': 'new_pwd',
                'tos': True}
        form = EmailUserCreationForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid(self):
        data_no_email = {'username': 'joebloggs', 'email': '', 'password1': 'new_pwd', 'password2': 'new_pwd',
                         'tos': True}
        data_invalid_email = {'username': 'joebloggs', 'email': '', 'password1': 'new_pwd', 'password2': 'new_pwd',
                              'tos': True}
        data_no_tos = {'username': 'joebloggs', 'email': 'joe@example.org', 'password1': 'new_pwd',
                       'password2': 'new_pwd'}
        data_false_tos = {'username': 'joebloggs', 'email': 'joe@example.org', 'password1': 'new_pwd',
                          'password2': 'new_pwd', 'tos': False}

        form = EmailUserCreationForm(data=data_no_email)
        self.assertFalse(form.is_valid())
        form = EmailUserCreationForm(data=data_invalid_email)
        self.assertFalse(form.is_valid())
        self.assertEqual('This field is required.', form.errors['email'][0])
        form = EmailUserCreationForm(data=data_no_tos)
        self.assertFalse(form.is_valid())
        self.assertEqual('You must agree our Terms of Service', form.errors['tos'][0])
        form = EmailUserCreationForm(data=data_false_tos)
        self.assertFalse(form.is_valid())
        self.assertEqual('You must agree our Terms of Service', form.errors['tos'][0])


class TestPasswordResetForm(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.request_factory = RequestFactory()

    def test_valid(self):
        data = {'email': self.user.email}
        form = PasswordResetForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid(self):
        # Empty
        data = {'email': ''}
        form = PasswordResetForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual('This field is required.', form.errors['email'][0])

        # Invalid
        data = {'email': 'invalid@example.org'}
        form = PasswordResetForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual('Enter a valid email address', form.errors['email'][0])

        # Inactive
        user = UserFactory(is_active=False)
        data = {'email': user.email}
        form = PasswordResetForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual('Enter a valid email address', form.errors['email'][0])

        # Disabled password
        user = UserFactory()
        user.set_unusable_password()
        user.save()
        data = {'email': user.email}
        form = PasswordResetForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual('Enter a valid email address', form.errors['email'][0])

    def test_save(self):
        data = {'email': self.user.email}
        request = self.request_factory.post(reverse('password-reset'), data=data)
        form = PasswordResetForm(data=data)
        self.assertTrue(form.is_valid())
        form.save(request=request)
        self.assertEqual(len(mail.outbox), 1)

    def test_save_multi(self):
        user1 = UserFactory(email='joe@example.org')
        UserFactory(email='joe@example.org')
        data = {'email': user1.email}
        request = self.request_factory.post(reverse('password-reset'), data=data)
        form = PasswordResetForm(data=data)
        self.assertTrue(form.is_valid())
        form.save(request=request)
        self.assertEqual(len(mail.outbox), 2)

    def test_token_generation(self):
        user = UserFactory()
        data = {'email': user.email}
        request = self.request_factory.post(reverse('password-reset'), data=data)
        reset_form = PasswordResetForm(data=data)
        self.assertTrue(reset_form.is_valid())
        context = reset_form.get_context_data(request, user, default_token_generator)
        uidb64, token = urlparse(context['url']).path.split('/')[-3:-1]
        self.assertIsNotNone(re.match("[0-9A-Za-z_\-]+", uidb64))
        self.assertIsNotNone(re.match("[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20}", token))
        self.assertEqual(urlsafe_base64_decode(uidb64).decode("utf-8"), str(user.id))
        self.assertTrue(default_token_generator.check_token(user, token))
