import string
import json
import copy
import factory

from django.test import TestCase
from django_webtest import WebTest
from django.core.urlresolvers import reverse

from cellcounter.keyboardapi.models import KeyMap, CustomKeyboard
from cellcounter.main.tests import UserFactory
from cellcounter.main.models import CellType
from cellcounter.keyboardapi.defaults import (DEFAULT_KEYBOARD_MAP,
                                              TEST_POST_KEYBOARD_MAP)


class KeyMapFactory(factory.DjangoModelFactory):
    FACTORY_FOR = KeyMap
    key = 'a'


class KeyboardFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = CustomKeyboard
    label = factory.Sequence(lambda n: "test%s" % n)
    user = factory.SubFactory(UserFactory)

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


class CustomKeyboardTestCase(TestCase):

    def test_unicode(self):
        keyboard = KeyboardFactory.build(user__username='alpha', label='alpha')
        self.assertEqual(keyboard.__unicode__(), 'Keyboard alpha for alpha')

    def test_get_mappings_json(self):
        keyboard = KeyboardFactory(add_maps=False)
        mapping = KeyMapFactory(cellid=CellType.objects.get(id=1))
        keyboard.mappings.add(mapping)
        keyboard.save()
        self.assertEqual('{"a": {"cellid": 1}}', keyboard.get_mappings_json())

    def test_set_primary_self(self):
        keyboard = KeyboardFactory(add_maps=False)
        keyboard.set_primary()
        self.assertTrue(CustomKeyboard.objects.get(id=keyboard.id).is_primary)

    def test_set_primary_other(self):
        user = UserFactory()
        keyboard1 = KeyboardFactory(user=user, is_primary=True, add_maps=False)
        keyboard2 = KeyboardFactory(user=user, add_maps=False)

        self.assertTrue(keyboard1.is_primary)
        self.assertFalse(CustomKeyboard.objects.get(id=keyboard2.id).is_primary)

        keyboard2.set_primary()
        self.assertTrue(CustomKeyboard.objects.get(id=keyboard2.id).is_primary)
        self.assertFalse(CustomKeyboard.objects.get(id=keyboard1.id).is_primary)

    def test_delete_no_primary(self):
        keyboard = KeyboardFactory(add_maps=False)
        keyboard.delete()
        self.assertEqual(len(CustomKeyboard.objects.all()), 0)

    def test_delete_change_primary(self):
        user = UserFactory()
        keyboard1 = KeyboardFactory(user=user, is_primary=True, add_maps=False)
        keyboard2 = KeyboardFactory(user=user, add_maps=False)

        keyboard1.delete()
        self.assertEqual(len(CustomKeyboard.objects.all()), 1)
        self.assertTrue(CustomKeyboard.objects.get(id=keyboard2.id).is_primary)

class KeyboardAPITestCase(WebTest):

    def setUp(self):
        keyboard = KeyboardFactory(user__username='example', is_primary=True,
                                   add_maps=False)
        self.keyboard_id = keyboard.id
        self.user = keyboard.user
        mapping = KeyMap(cellid=CellType.objects.get(id=1), key='a')
        mapping.save()
        keyboard.mappings.add(mapping)
        UserFactory.create(username='alternate')

    def test_get_logged_out_default(self):
        response = self.app.get(reverse('base_keyboard'))
        self.assertEqual(response.body, json.dumps(DEFAULT_KEYBOARD_MAP))

    def test_get_logged_out_other_denied(self):
        response = self.app.get(reverse('select_keyboard',
                                        kwargs={'pk': self.keyboard_id}),
                                status=403)
        self.assertEqual(response.status_int, 403)

    def test_get_logged_in_primary(self):
        response = self.app.get(reverse('base_keyboard'), user='example')
        self.assertEqual(response.body, '{"a": {"cellid": 1}}')

    def test_get_logged_in_own_other(self):
        keyboard2 = KeyboardFactory(user=self.user, add_maps=False)
        mapping = KeyMap(cellid=CellType.objects.get(id=1), key='a')
        mapping.save()
        keyboard2.mappings.add(mapping)
        response = self.app.get(reverse('select_keyboard',
                                        kwargs={'pk': keyboard2.id}),
                                user='example')
        self.assertEqual(response.body, '{"a": {"cellid": 1}}')

    def test_get_logged_in_other_denied(self):
        response = self.app.get(reverse('select_keyboard',
                                        kwargs={'pk': self.keyboard_id}),
                                user='alternate', status=403)
        self.assertEqual(response.status_int, 403)

    def test_post_logged_out_denied(self):
        response = self.app.post(reverse('base_keyboard'),
                                      json.dumps(DEFAULT_KEYBOARD_MAP),
                                      status=403)
        self.assertEqual(response.status_int, 403)

    def test_post_logged_in_wellformed(self):
        response = self.app.post(reverse('base_keyboard'),
                                 json.dumps(TEST_POST_KEYBOARD_MAP),
                                 user='example', status=204)
        self.assertEqual(response.status_int, 204)

    def test_post_logged_in_malformed(self):
        """Only keys mapping to [a-z] are permitted. "cellid" is the only
        permitted key for each key, and must correspond to a numerical value
        everything else should be rejected"""
        response = self.app.post(reverse('base_keyboard'),
                                 '', user='example', status=400)
        self.assertEqual(response.status_int, 400)
        self.assertEqual(response.body, 'Malformed or invalid JSON presented')

        # Reject random string
        response = self.app.post(reverse('base_keyboard'),
                                 'hello', user='example', status=400)
        self.assertEqual(response.status_int, 400)
        self.assertEqual(response.body, 'Malformed or invalid JSON presented')

        # Reject nonnumeric cellids
        response = self.app.post(reverse('base_keyboard'),
                                 json.dumps({"a": {"cellid": "a"}}),
                                 user='example', status=400)
        self.assertEqual(response.status_int, 400)
        self.assertEqual(response.body, 'Malformed or invalid JSON presented')

        # Reject additional params
        response = self.app.post(reverse('base_keyboard'),
                                 json.dumps({"a": {"cellid": 1, "test": "a"}}),
                                 user='example', status=400)
        self.assertEqual(response.status_int, 400)
        self.assertEqual(response.body, 'Malformed or invalid JSON presented')

        # Reject with no cellid map provided
        response = self.app.post(reverse('base_keyboard'),
                                 json.dumps({"a": {}}),
                                 user='example', status=400)
        self.assertEqual(response.status_int, 400)
        self.assertEqual(response.body, 'Malformed or invalid JSON presented')

        # Reject non [a-z] keymapping
        response = self.app.post(reverse('base_keyboard'),
                                 json.dumps({"1": {"cellid": 1}}),
                                 user='example', status=400)
        self.assertEqual(response.status_int, 400)
        self.assertEqual(response.body, 'Malformed or invalid JSON presented')

    def test_post_logged_in_extra_cell(self):
        keyboard_map = copy.copy(TEST_POST_KEYBOARD_MAP)
        keyboard_map['l'] = {"cellid": 92}
        response = self.app.post(reverse('base_keyboard'),
                                 json.dumps(keyboard_map),
                                 user='example', status=400)
        self.assertEqual(response.body, 'Nonexistent celltype mapping requested')