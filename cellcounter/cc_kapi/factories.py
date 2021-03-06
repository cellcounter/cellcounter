import string

import factory
from django.contrib.auth.models import User

from cellcounter.main.models import CellType
from . import models


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: "test%s" % n)
    first_name = factory.Sequence(lambda n: "test%s" % n)
    last_name = factory.Sequence(lambda n: "test%s" % n)
    email = factory.Sequence(lambda n: "test%s@example.com" % n)
    password = factory.PostGenerationMethodCall('set_password', 'test')

    is_staff = False
    is_active = True
    is_superuser = False


class KeyboardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Keyboard

    user = factory.SubFactory(UserFactory)
    label = 'Test'
    is_primary = False

    @factory.post_generation
    def add_maps(self, create, extracted, **kwargs):
        if not create:
            return
        if not extracted:
            return
        i = 0
        for cell in CellType.objects.all():
            mapping, created = models.KeyMap.objects.get_or_create(
                cellid=cell, key=string.ascii_lowercase[i])
            self.mappings.add(mapping)
            i += 1

        self.save()


class KeyMapFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.KeyMap

    key = 'a'