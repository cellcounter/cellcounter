from django_webtest import WebTest
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.core import mail
from django.test.utils import override_settings
from django.utils.translation import ugettext as _
from django.test.client import RequestFactory

from cellcounter.cc_kapi.factories import UserFactory, KeyboardFactory
from cellcounter.cc_kapi.models import Keyboard
from cellcounter.accounts.forms import PasswordResetForm


class RegistrationViewTest(TestCase):
    client = Client()
    full_form = {'username': 'Example', 'email': 'user@example.org',
                 'password1': 'test', 'password2': 'test', 'tos': True}
    no_tos = {'username': 'Example', 'email': 'user@example.org',
              'password1': 'test', 'password2': 'test'}
    wrong_pwd = {'username': 'Example', 'email': 'user@example.org',
                 'password1': 'test', 'password2': 'notest', 'tos': True}
    invalid_email = {'username': 'Example', 'email': 'user@',
                     'password1': 'test', 'password2': 'test', 'tos': True}

    def test_get_register(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_empty_registration(self):
        response = self.client.post(reverse('register'), {})
        self.assertIn('This field is required', response.content)

    def test_successful_registration(self):
        response = self.client.post(reverse('register'), self.full_form)
        self.assertTrue('Successfully registered' in response.cookies['messages'].value)

    def test_no_tos(self):
        response = self.client.post(reverse('register'), self.no_tos)
        self.assertIn('You must agree our Terms of Service', response.content)
        self.assertEqual(response.context['user'].username, '')

    def test_mismatched_passwords(self):
        response = self.client.post(reverse('register'), self.wrong_pwd)
        self.assertIn('The two password fields didn&#39;t match.', response.content)
        self.assertEqual(response.context['user'].username, '')

    def test_non_unique_username(self):
        user = UserFactory(username='Example')
        response = self.client.post(reverse('register'), self.full_form)
        self.assertIn('A user with that username already exists', response.content)
        self.assertEqual(response.context['user'].username, '')

    def test_invalid_email(self):
        response = self.client.post(reverse('register'), self.invalid_email)
        self.assertIn('Enter a valid email address', response.content)
        self.assertEqual(response.context['user'].username, '')

    def test_login_on_register(self):
        response = self.client.post(reverse('register'), self.full_form, follow=True)
        self.assertIn('Logout', response.content)
        self.assertEqual(response.context['user'].username, 'Example')

    @override_settings(RATELIMIT_ENABLE=True)
    def test_ratelimit(self):
        self.client.post(reverse('register'), self.full_form)
        self.client.logout()
        form_data = self.full_form
        form_data['username'] = 'Another'
        response = self.client.post(reverse('register'), form_data, follow=True)
        self.assertNotIn('Successfully registered', response.content)
        self.assertIn('You have been rate limited', response.content)


class PasswordChangeViewTest(WebTest):
    def setUp(self):
        self.user = UserFactory()

    def _get_pwd_change_form(self):
        return self.app.get(reverse('change-password'),
                            user=self.user.username).form

    def test_get_change_pwd_logged_out(self):
        response = self.app.get(reverse('change-password')).follow()
        self.assertEqual(response.status_code, 200)
        self.assertIn('<label class="control-label" for="username">Username</label>', response.body)

    def test_get_change_pwd_logged_in(self):
        user = UserFactory()
        response = self.app.get(reverse('change-password'), user=user.username)
        self.assertEqual(response.status_code, 200)
        self.assertIn('<input type="submit" class="btn btn-success" value="Change Password">', response.body)

    def test_pwd_change_correct(self):
        form = self._get_pwd_change_form()
        form['old_password'] = 'test'
        form['new_password1'] = 'new'
        form['new_password2'] = 'new'
        response = form.submit()
        self.assertIn('Password changed successfully', response.headers['Set-Cookie'])

        response = self.app.get(reverse('logout')).follow()
        self.assertEqual(response.context['user'].username, '')

        # Login with new password
        form = self.app.get(reverse('login')).form
        form['username'] = self.user.username
        form['password'] = 'new'
        response = form.submit().follow()
        self.assertEqual(response.context['user'].username, self.user.username)

    def test_pwd_change_wrong_pwd(self):
        form = self._get_pwd_change_form()
        form['old_password'] = 'new'
        form['new_password1'] = 'new'
        form['new_password2'] = 'new'
        response = form.submit()
        self.assertIn('Your old password was entered incorrectly', response.body)

    def test_pwd_change_mismatched_pwd(self):
        form = self._get_pwd_change_form()
        form['old_password'] = 'test'
        form['new_password1'] = 'new'
        form['new_password2'] = 'new2'
        response = form.submit()
        self.assertIn('The two password fields didn&#39;t match', response.body)


class UserManagementTest(WebTest):
    csrf_checks = False

    def setUp(self):
        self.user = UserFactory()

    def test_get_own_profile(self):
        response = self.app.get(
            reverse('user-detail', kwargs={'pk': self.user.id}),
            user=self.user)
        self.assertEquals(200, response.status_code)

    def test_get_other_profile(self):
        user2 = UserFactory()
        response = self.app.get(
            reverse('user-detail', kwargs={'pk': self.user.id}),
            user=user2, status=403)
        self.assertEquals(403, response.status_code)

    def test_delete_logged_out(self):
        user2 = UserFactory()
        response = self.app.post(
            reverse('user-delete', kwargs={'pk': user2.id}),
            status=403)
        self.assertEquals(403, response.status_code)

    def test_get_delete_own_user(self):
        user2 = UserFactory()
        response = self.app.get(
            reverse('user-delete', kwargs={'pk': user2.id}),
            user=user2
        )
        self.assertEquals(200, response.status_code)
        self.assertIn('Are you sure you want to delete', response.body)

    def test_get_delete_other_user(self):
        user2 = UserFactory()
        response = self.app.get(
            reverse('user-delete', kwargs={'pk': user2.id}),
            user=self.user, status=403
        )
        self.assertEquals(403, response.status_code)

    def test_post_delete_own_user(self):
        user2 = UserFactory()
        keyboard = KeyboardFactory(is_primary=True, user=user2)
        self.assertEquals(keyboard, Keyboard.objects.get(id=keyboard.id))
        response = self.app.post(
            reverse('user-delete', kwargs={'pk': user2.id}),
            user=user2
        )
        self.assertEquals(302, response.status_code)
        with self.assertRaises(Keyboard.DoesNotExist):
            Keyboard.objects.get(id=keyboard.id)

    def test_post_delete_other_user(self):
        user2 = UserFactory()
        response = self.app.post(
            reverse('user-delete', kwargs={'pk': user2.id}),
            user=self.user, status=403
        )
        self.assertEquals(403, response.status_code)


class PasswordReset(WebTest):
    # csrf_checks = False

    def setUp(self):
        self.user = UserFactory()
        self.factory = RequestFactory()

    def test_invalid_email(self):
        data = {'email': 'not valid'}
        form = PasswordResetForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form['email'].errors, [_('Enter a valid email address.')])

    def test_nonexistant_email(self):
        """
        Test nonexistent email address. This should not fail because it would
        expose information about registered users.
        """
        data = {'email': 'foo@bar.com'}
        form = PasswordResetForm(data)
        self.assertTrue(form.is_valid())
        self.assertEqual(len(mail.outbox), 0)

    def test_inactive_user(self):
        """
        Test that inactive user cannot receive password reset email.
        """
        user = UserFactory(is_active=False)
        form = PasswordResetForm({'email': user.email})
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(len(mail.outbox), 0)

    def test_unusable_password(self):
        user = UserFactory()
        data = {"email": user.email}
        form = PasswordResetForm(data)
        self.assertTrue(form.is_valid())
        user.set_unusable_password()
        user.save()
        form = PasswordResetForm(data)
        # The form itself is valid, but no email is sent
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(len(mail.outbox), 0)

    def test_password_reset_form(self):
        form_data = {'email': self.user.email}
        form = PasswordResetForm(data=form_data)
        self.assertEqual(form.is_valid(), True)
        request = self.factory.post(reverse('password-reset'), data={'email': self.user.email})
        form.save(request=request)
        self.assertEqual(form.cleaned_data['email'], self.user.email)
        self.assertEqual(len(mail.outbox), 1)