import factory

from django_webtest import WebTest
from django.test import TestCase
from django.core.urlresolvers import reverse

from cellcounter.cc_kapi.factories import UserFactory, KeyboardFactory
from cellcounter.cc_kapi.models import Keyboard
from .models import LicenseAgreement, UserLicenseAgreement


class LicenseFactory(factory.DjangoModelFactory):
    FACTORY_FOR = LicenseAgreement
    title = factory.Sequence(lambda n: "License Agreement%s" % n)
    text = "License agreement text"


class LicenseAgreementTest(TestCase):
    def setUp(self):
        self.license = LicenseFactory()

    def test_is_active(self):
        self.assertTrue(self.license.is_active)

    def test_set_active(self):
        license = LicenseFactory(is_active=False)
        self.assertFalse(license.is_active)
        license.set_active()
        self.assertTrue(license.is_active)

    def test_sync_active(self):
        license = LicenseFactory()
        self.assertTrue(self.license.is_active)
        self.assertTrue(license.is_active)
        license.set_active()
        self.assertTrue(license.is_active)
        self.assertFalse(
            LicenseAgreement.objects.get(id=self.license.id).is_active)
        self.license.set_active()
        self.assertTrue(
            LicenseAgreement.objects.get(id=self.license.id).is_active)
        self.assertFalse(
            LicenseAgreement.objects.get(id=license.id).is_active)

    def test_get_html(self):
        license = LicenseFactory()
        self.assertEqual('<p>License agreement text</p>\n', license.get_html_text())


class LicenseViewTest(WebTest):
    def test_get_license_no_license(self):
        response = self.app.get(reverse('latest-license'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(None, response.context['object'])
        self.assertIn('No License set', response.body)

    def test_get_license_license(self):
        license = LicenseFactory()
        response = self.app.get(reverse('latest-license'))
        self.assertNotEqual(None, response.context['object'])
        self.assertEqual(license, response.context['object'])
        self.assertIn(license.title, response.body)

    def test_race_license(self):
        """Ugly test, required due to potential for two active licenses to be
        present whilst waiting for LicenseAgreement._sync_active() to be called.
        Ensure that only the latest active license is returned, and display
        does not break should this occur."""
        LicenseFactory(is_active=True)
        license2 = LicenseFactory(is_active=True)
        response = self.app.get(reverse('latest-license'))
        self.assertNotEqual(None, response.context['object'])
        self.assertEqual(license2, response.context['object'])
        self.assertIn(license2.title, response.body)

    def test_get_specific_license(self):
        license = LicenseFactory()
        response = self.app.get(reverse('license-detail', kwargs={'pk': license.id}))
        self.assertEqual(200, response.status_code)
        self.assertEqual(license, response.context['license'])
        self.assertEqual(license.get_html_text(), response.context['license_text'])


class RegistrationViewTest(WebTest):
    def setUp(self):
        self.license = LicenseFactory()

    def _get_registration_form(self):
        return self.app.get(reverse('register')).form

    def test_get_register(self):
        response = self.app.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_empty_registration(self):
        form = self._get_registration_form()
        response = form.submit()
        self.assertIn('This field is required', response.body)

    def test_successful_registration(self):
        form = self._get_registration_form()
        form['username'] = 'Example'
        form['email'] = 'user@example.com'
        form['password1'] = 'test'
        form['password2'] = 'test'
        form['tos'] = True
        response = form.submit()
        self.assertIn('Successfully registered', response.headers['Set-Cookie'])

    def test_no_tos(self):
        form = self._get_registration_form()
        form['username'] = 'Example'
        form['email'] = 'user@example.com'
        form['password1'] = 'test'
        form['password2'] = 'test'
        form['tos'] = False
        response = form.submit()
        self.assertIn('You must agree our Terms of Service', response.body)
        self.assertEqual(response.context['user'].username, '')

    def test_mismatched_passwords(self):
        form = self._get_registration_form()
        form['username'] = 'Example'
        form['email'] = 'user@example.com'
        form['password1'] = 'test'
        form['password2'] = 'test2'
        form['tos'] = True
        response = form.submit()
        self.assertIn('The two password fields didn&#39;t match.', response.body)
        self.assertEqual(response.context['user'].username, '')

    def test_non_unique_username(self):
        form = self._get_registration_form()
        user = UserFactory()
        form['username'] = user.username
        form['email'] = 'user@example.com'
        form['password1'] = 'test'
        form['password2'] = 'test'
        form['tos'] = True
        response = form.submit()
        self.assertIn('A user with that username already exists', response.body)
        self.assertEqual(response.context['user'].username, '')

    def test_invalid_email(self):
        form = self._get_registration_form()
        form['username'] = 'Example'
        form['email'] = 'user@'
        form['password1'] = 'test'
        form['password2'] = 'test'
        form['tos'] = True
        response = form.submit()
        self.assertIn('Enter a valid email address', response.body)
        self.assertEqual(response.context['user'].username, '')

    def test_login_on_register(self):
        form = self._get_registration_form()
        form['username'] = 'Example'
        form['email'] = 'user@example.com'
        form['password1'] = 'test'
        form['password2'] = 'test'
        form['tos'] = True
        response = form.submit().follow()
        self.assertIn('Logout', response.body)
        self.assertEqual(response.context['user'].username, 'Example')


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
        self.license = LicenseFactory()
        self.agreement = UserLicenseAgreement(user=self.user, license=self.license).save()

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