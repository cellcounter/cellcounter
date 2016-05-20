import factory
import string
from django.contrib.auth.models import User

from cellcounter.main.models import CellType
from .models import Keyboard, KeyMap


class UserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = User

    username = factory.Sequence(lambda n: "test%s" % n)
    first_name = factory.Sequence(lambda n: "test%s" % n)
    last_name = factory.Sequence(lambda n: "test%s" % n)
    email = factory.Sequence(lambda n: "test%s@example.com" % n)
    password = factory.PostGenerationMethodCall('set_password', 'test')

    is_staff = False
    is_active = True
    is_superuser = False


class KeyboardFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Keyboard

    user = factory.SubFactory(UserFactory)
    label = 'Test'
    is_default = False

    @factory.post_generation
    def add_maps(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted == False:
            return
        i = 0
        for cell in CellType.objects.all():
            mapping, created = KeyMap.objects.get_or_create(
                cellid=cell, key=string.ascii_lowercase[i])
            self.mappings.add(mapping)
            i = i+1

        self.save()


class KeyMapFactory(factory.DjangoModelFactory):
    FACTORY_FOR = KeyMap
    key = 'a'
