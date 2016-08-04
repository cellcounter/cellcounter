import string

import factory

from cellcounter.cc_kapi.models import Keyboard, KeyMap
from cellcounter.main.factories import UserFactory
from cellcounter.main.models import CellType


class KeyboardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Keyboard

    user = factory.SubFactory(UserFactory)
    label = 'Test'
    is_primary = False

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


class KeyMapFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = KeyMap

    key = 'a'