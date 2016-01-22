from urlparse import urlparse

from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth.tokens import default_token_generator
from django.core import mail
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import RequestFactory
from django.test.utils import override_settings
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from cellcounter.cc_kapi.factories import UserFactory, KeyboardFactory
from .forms import EmailUserCreationForm, PasswordResetForm
from .utils import read_signup_email
from .views import PasswordResetConfirmView


class TestRegistrationView(TestCase):

    def setUp(self):
        self.request_factory = RequestFactory()

    def test_get(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], EmailUserCreationForm)

    def test_valid(self):
        data = {'username': '123', 'email': 'joe@example.org', 'password1': 'test', 'password2': 'test', 'tos': True}
        response = self.client.post(reverse('register'), data=data, follow=True)
        self.assertRedirects(response, reverse('new_count'))
        messages = list(response.context['messages'])
        self.assertEqual("Successfully registered, you are now logged in! <a href='/accounts/1/'>View your profile</a>",
                         messages[0].message)
        user = User.objects.get(username='123')
        self.assertEqual(user, response.context['user'])

    def test_invalid(self):
        data = {'username': '123', 'email': 'joe@example.org', 'password1': 'test', 'password2': 'test', 'tos': False}
        response = self.client.post(reverse('register'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'tos', 'You must agree our Terms of Service')
        self.assertEqual(AnonymousUser(), response.context['user'])

    @override_settings(RATELIMIT_ENABLE=True)
    def test_ratelimit_registration(self):
        cache.clear()
        data = {'username': '123', 'email': 'joe@example.org', 'password1': 'test', 'password2': 'test', 'tos': True}
        self.client.post(reverse('register'), data)
        self.client.logout()
        data['username'] = 'Another'
        self.client.post(reverse('register'), data, follow=True)
        self.client.logout()
        data['username'] = 'Another2'
        response = self.client.post(reverse('register'), data, follow=True)
        messages = list(response.context['messages'])
        self.assertEqual(1, len(messages))
        self.assertEqual('You have been rate limited', messages[0].message)

    @override_settings(RATELIMIT_ENABLE=True)
    def test_ratelimit_invalid_form(self):
        cache.clear()
        data = {'username': '123', 'email': '1234', 'password1': 'test', 'password2': 'test', 'tos': True}
        self.client.post(reverse('register'), data)
        response = self.client.post(reverse('register'), data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('You have been rate limited', response.content)


class TestPasswordChangeView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = UserFactory()
        self.valid_data = {'old_password': 'test', 'new_password1': 'new', 'new_password2': 'new'}
        self.invalid_data = {'old_password': 'test', 'new_password1': 'test', 'new_password2': '1234'}

    def test_logged_out_get_redirect(self):
        response = self.client.get(reverse('change-password'))
        self.assertRedirects(response,
                             "%s?next=%s" % (reverse('login'), reverse('change-password')))

    def test_logged_out_post_redirect(self):
        response = self.client.post(reverse('change-password'), self.valid_data)
        self.assertRedirects(response,
                             "%s?next=%s" % (reverse('login'), reverse('change-password')))

    def test_logged_in_to_form(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('change-password'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], PasswordChangeForm)

    def test_post_valid(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('change-password'), data=self.valid_data, follow=True)
        self.assertRedirects(response, reverse('new_count'))
        messages = list(response.context['messages'])
        self.assertEqual('Password changed successfully', messages[0].message)

    def test_post_invalid(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('change-password'), data=self.invalid_data)
        self.assertFormError(response, 'form', 'new_password2', "The two password fields didn't match.")


class TestUserDetailView(TestCase):
    def setUp(self):
        self.keyboard = KeyboardFactory()

    def test_get_anonymous(self):
        user2 = UserFactory()
        response = self.client.get(reverse('user-detail', kwargs={'pk': user2.id}))
        self.assertRedirects(response,
                             "%s?next=%s" % (reverse('login'), reverse('user-detail', kwargs={'pk': user2.id})))

    def test_get_self(self):
        self.client.force_login(self.keyboard.user)
        response = self.client.get(reverse('user-detail', kwargs={'pk': self.keyboard.user.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user_detail'], self.keyboard.user)
        self.assertEqual(len(response.context['keyboards']), 1)

    def test_get_someone_else(self):
        user2 = UserFactory()
        self.client.force_login(self.keyboard.user)
        response = self.client.get(reverse('user-detail', kwargs={'pk': user2.id}))
        self.assertEqual(response.status_code, 403)


class TestUserDeleteView(TestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_get_delete_anonymous(self):
        response = self.client.get(reverse('user-delete', kwargs={'pk': self.user.id}))
        self.assertRedirects(response,
                             "%s?next=%s" % (reverse('login'), reverse('user-delete', kwargs={'pk': self.user.id})))

    def test_delete_anonymous(self):
        user2 = UserFactory()
        response = self.client.delete(reverse('user-delete', kwargs={'pk': user2.id}))
        self.assertRedirects(response,
                             "%s?next=%s" % (reverse('login'), reverse('user-delete', kwargs={'pk': user2.id})))

    def test_get_delete_self(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('user-delete', kwargs={'pk': self.user.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/user_check_delete.html')

    def test_delete_self(self):
        self.client.force_login(self.user)
        response = self.client.delete(reverse('user-delete', kwargs={'pk': self.user.id}), follow=True)
        self.assertRedirects(response, reverse('new_count'))
        self.assertEqual('User account deleted', list(response.context['messages'])[0].message)

    def test_get_delete_someone_else(self):
        user2 = UserFactory()
        self.client.force_login(self.user)
        response = self.client.get(reverse('user-delete', kwargs={'pk': user2.id}))
        self.assertEqual(response.status_code, 403)

    def test_delete_someone_else(self):
        user2 = UserFactory()
        self.client.force_login(self.user)
        response = self.client.delete(reverse('user-delete', kwargs={'pk': user2.id}))
        self.assertEqual(response.status_code, 403)


class TestUserUpdateView(TestCase):
    def setUp(self):
        self.valid_data = {'first_name': 'Jack', 'last_name': 'Example', 'email': 'test@example.org'}
        self.extra_data = {'first_name': 'Joe', 'last_name': 'Example', 'email': 'test@example.org',
                           'username': 'invalid'}
        self.invalid_data = {'first_name': 'Joe', 'last_name': 'Example', 'email': '1234'}

    def test_get_update_when_anonymous(self):
        user = UserFactory()
        response = self.client.get(reverse('user-update', kwargs={'pk': user.id}))
        self.assertRedirects(response,
                             "%s?next=%s" % (reverse('login'), reverse('user-update', kwargs={'pk': user.id})))

    def test_post_update_when_anonymous(self):
        user = UserFactory()
        response = self.client.post(reverse('user-update', kwargs={'pk': user.id}), data=self.valid_data)
        self.assertRedirects(response,
                             "%s?next=%s" % (reverse('login'), reverse('user-update', kwargs={'pk': user.id})))

    def test_update_self_valid(self):
        user = UserFactory()
        self.client.force_login(user)
        response = self.client.post(reverse('user-update', kwargs={'pk': user.id}), data=self.valid_data,
                                    follow=True)
        self.assertRedirects(response, reverse('user-detail', kwargs={'pk': user.id}))
        self.assertEqual('User details updated', list(response.context['messages'])[0].message)
        updated_user = User.objects.get(username=user.username)
        self.assertNotEqual(updated_user.first_name, user.first_name)
        self.assertNotEqual(updated_user.last_name, user.last_name)
        self.assertNotEqual(updated_user.email, user.email)

    def test_update_self_extra(self):
        user = UserFactory()
        self.client.force_login(user)
        response = self.client.post(reverse('user-update', kwargs={'pk': user.id}), data=self.extra_data,
                                    follow=True)
        self.assertRedirects(response, reverse('user-detail', kwargs={'pk': user.id}))
        self.assertEqual('User details updated', list(response.context['messages'])[0].message)
        updated_user = User.objects.get(username=user.username)
        self.assertNotEqual(updated_user.first_name, user.first_name)
        self.assertNotEqual(updated_user.last_name, user.last_name)
        self.assertNotEqual(updated_user.email, user.email)
        self.assertEqual(updated_user.username, user.username)

    def test_update_self_invalid(self):
        user = UserFactory()
        self.client.force_login(user)
        response = self.client.post(reverse('user-update', kwargs={'pk': user.id}), data=self.invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'email', 'Enter a valid email address.')

    def test_update_someone_else(self):
        user = UserFactory()
        user2 = UserFactory()
        self.client.force_login(user)
        response = self.client.post(reverse('user-update', kwargs={'pk': user2.id}))
        self.assertEqual(response.status_code, 403)


class TestPasswordResetView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = UserFactory()

    def test_get_form(self):
        response = self.client.get(reverse('password-reset'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], PasswordResetForm)
        self.assertTemplateUsed(response, 'accounts/reset_form.html')

    def test_post_valid_email(self):
        data = {'email': self.user.email}
        response = self.client.post(reverse('password-reset'), data=data, follow=True)
        self.assertRedirects(response, reverse('new_count'))
        self.assertEqual('Reset email sent', list(response.context['messages'])[0].message)
        self.assertEqual(1, len(mail.outbox))
        url, path = read_signup_email(mail.outbox[0])
        uidb64, token = urlparse(url).path.split('/')[-3:-1]
        self.assertEqual(path, reverse('password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token}))

    def test_post_invalid_email(self):
        data = {'email': 'invalid@example.org'}
        response = self.client.post(reverse('password-reset'), data=data, follow=True)
        self.assertRedirects(response, reverse('new_count'))
        self.assertEqual(0, len(mail.outbox))

    @override_settings(RATELIMIT_ENABLE=True)
    def test_post_ratelimit(self):
        for n in range(0, 5):
            self.client.post(reverse('password-reset'), data={'email': self.user.email}, follow=True)
        response = self.client.post(reverse('password-reset'), data={'email': self.user.email}, follow=True)
        self.assertEqual(list(response.context['messages'])[0].message, 'You have been rate limited')
        cache.clear()


class TestPasswordResetConfirmView(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.valid_uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.valid_data = {'new_password1': 'newpwd', 'new_password2': 'newpwd'}
        self.invalid_data = {'new_password1': 'newpwd', 'new_password2': '1234'}

    def _generate_token(self, user):
        return default_token_generator.make_token(user)

    def test_valid_user_valid(self):
        """valid_user() with valid uidb64"""
        self.assertEqual(PasswordResetConfirmView().valid_user(self.valid_uidb64), self.user)

    def test_valid_user_invalid(self):
        """valid_user() with invalid uidb64"""
        uidb64 = urlsafe_base64_encode(force_bytes(2))
        self.assertIsNone(PasswordResetConfirmView().valid_user(uidb64))

    def test_valid_token_valid(self):
        """valid_token() with valid user and token"""
        self.assertTrue(PasswordResetConfirmView().valid_token(self.user, self._generate_token(self.user)))

    def test_valid_token_invalid_token(self):
        """valid_token() with valid user and invalid token"""
        token = "AAA-AAAAAAAAAAAAAAAAAAAA"
        self.assertFalse(PasswordResetConfirmView().valid_token(self.user, token))

    def test_valid_token_invalid_both(self):
        """valid_token() with invalid user and invalid token"""
        token = "AAA-AAAAAAAAAAAAAAAAAAAA"
        self.assertFalse(PasswordResetConfirmView().valid_token(None, self._generate_token(self.user)))

    def test_get_invalid_token(self):
        token = "AAA-AAAAAAAAAAAAAAAAAAAA"
        response = self.client.get(reverse('password-reset-confirm',
                                           kwargs={'uidb64': self.valid_uidb64,
                                                   'token': token}))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['validlink'])
        self.assertIn("The password reset link was invalid, possibly because it has already been used."
                      " Please request a new password reset.", response.content)

    def test_get_invalid_user(self):
        response = self.client.get(reverse('password-reset-confirm',
                                           kwargs={'uidb64': urlsafe_base64_encode(force_bytes(2)),
                                                   'token': self._generate_token(self.user)}))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['validlink'])
        self.assertIn("The password reset link was invalid, possibly because it has already been used."
                      " Please request a new password reset.", response.content)

    def test_post_invalid_token(self):
        token = "AAA-AAAAAAAAAAAAAAAAAAAA"
        response = self.client.post(reverse('password-reset-confirm',
                                            kwargs={'uidb64': self.valid_uidb64,
                                                    'token': token}),
                                    data=self.valid_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['validlink'])
        self.assertIn("The password reset link was invalid, possibly because it has already been used."
                      " Please request a new password reset.", response.content)

    def test_get_valid(self):
        token = self._generate_token(self.user)
        response = self.client.get(reverse('password-reset-confirm',
                                           kwargs={'uidb64': self.valid_uidb64,
                                                   'token': token}))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], SetPasswordForm)

    def test_post_valid(self):
        token = self._generate_token(self.user)
        response = self.client.post(reverse('password-reset-confirm',
                                            kwargs={'uidb64': self.valid_uidb64,
                                                    'token': token}),
                                    data=self.valid_data, follow=True)
        self.assertRedirects(response, reverse('new_count'))
        self.assertEqual('Password reset successfully', list(response.context['messages'])[0].message)

    def test_post_invalid(self):
        token = self._generate_token(self.user)
        response = self.client.post(reverse('password-reset-confirm',
                                            kwargs={'uidb64': self.valid_uidb64,
                                                    'token': token}),
                                    data=self.invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'new_password2', "The two password fields didn't match.")
