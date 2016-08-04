from datetime import datetime

import factory
import factory.fuzzy
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone

from cellcounter.main.models import CellType


def _get_tzinfo():
    """Fetch the current timezone."""
    if settings.USE_TZ:
        return timezone.get_current_timezone()
    else:
        return None


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: "test%s" % n)
    first_name = factory.fuzzy.FuzzyText(length=6)
    last_name = factory.fuzzy.FuzzyText(length=6)
    email = factory.Faker('email')
    password = factory.PostGenerationMethodCall('set_password', 'test')

    is_active = True
    is_staff = False
    is_superuser = False

    last_login = factory.fuzzy.FuzzyDateTime(datetime(2000, 1, 1, tzinfo=_get_tzinfo()))
    date_joined = factory.fuzzy.FuzzyDateTime(datetime(2000, 1, 1, tzinfo=_get_tzinfo()))


class CellTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CellType

    readable_name = 'test'
    machine_name = 'test'
    abbr_name = 'test'
    comment = "Test"
    visualisation_colour = '#FFFFFF'
