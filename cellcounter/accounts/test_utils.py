from django.test import TestCase
from django.test.client import RequestFactory

from cellcounter.cc_kapi.factories import UserFactory
from .forms import PasswordResetForm
from .utils import read_signup_email


class Email:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class TestReadEmailUtil(TestCase):
    def test_matching_email(self):
        user = UserFactory()
        request = RequestFactory().post("/")
        url = PasswordResetForm().get_context_data(request, user)["url"]
        msg = Email(body=url)
        email_url, path = read_signup_email(msg)
        self.assertEqual(email_url, url)

    def test_nonmatching_email(self):
        msg = Email(body="")
        email_url, path = read_signup_email(msg)
        self.assertTrue(not any([email_url, path]))
