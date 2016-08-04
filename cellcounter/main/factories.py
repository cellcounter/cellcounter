import factory
import factory.fuzzy
from django.contrib.auth.models import User

from cellcounter.main.models import CellType


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


class CellTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CellType

    readable_name = 'test'
    machine_name = 'test'
    abbr_name = 'test'
    comment = "Test"
    visualisation_colour = '#FFFFFF'
