import json

from django_webtest import WebTest
from django.test import TestCase

from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from rest_framework.renderers import JSONRenderer

from cellcounter.main.models import CellType
from .defaults import MOCK_KEYBOARD, DEFAULT_KEYBOARD_STRING
from .factories import UserFactory, KeyboardFactory, KeyMapFactory
from .models import KeyMap, Keyboard
from .views import KeyboardGetUpdateDestroyView
from .serializers import KeyboardSerializer, KeyMapSerializer, KeyboardOnlySerializer


class KeyboardTestCase(TestCase):
    fixtures = ['initial_data.json']

    def test_unicode(self):
        keyboard = KeyboardFactory.build(user__username='alpha', label='alpha')
        self.assertEqual(keyboard.__unicode__(), 'Keyboard alpha for alpha')

    def test_set_primary_self(self):
        keyboard = KeyboardFactory(add_maps=False)
        keyboard.set_primary()
        self.assertTrue(Keyboard.objects.get(id=keyboard.id).is_primary)

    def test_set_primary_other(self):
        user = UserFactory()
        keyboard1 = KeyboardFactory(user=user, is_primary=True, add_maps=False)
        keyboard2 = KeyboardFactory(user=user, add_maps=False)

        self.assertTrue(keyboard1.is_primary)
        self.assertFalse(Keyboard.objects.get(id=keyboard2.id).is_primary)

        keyboard2.set_primary()
        self.assertTrue(Keyboard.objects.get(id=keyboard2.id).is_primary)
        self.assertFalse(Keyboard.objects.get(id=keyboard1.id).is_primary)

    def test_delete_no_primary(self):
        keyboard = KeyboardFactory(add_maps=False)
        keyboard.delete()
        self.assertEqual(len(Keyboard.objects.all()), 0)

    def test_delete_change_primary(self):
        user = UserFactory()
        keyboard1 = KeyboardFactory(user=user, is_primary=True, add_maps=False)
        keyboard2 = KeyboardFactory(user=user, add_maps=False)

        keyboard1.delete()
        self.assertEqual(len(Keyboard.objects.all()), 1)
        self.assertTrue(Keyboard.objects.get(id=keyboard2.id).is_primary)

    def test_set_keymaps(self):
        user = UserFactory()
        keyboard = KeyboardFactory(user=user, is_primary=True)
        number_old_maps = len(keyboard.mappings.all())
        new_maps = [KeyMapFactory(cellid=CellType.objects.get(id=1))]
        keyboard.set_keymaps(new_maps)

        self.assertNotEqual(number_old_maps, len(keyboard.mappings.all()))
        self.assertEqual(len(new_maps), len(keyboard.mappings.all()))


class DefaultKeyboardAPITest(WebTest):
    fixtures = ['initial_data.json']
    csrf_checks = False

    def setUp(self):
        self.user = UserFactory()
        self.keyboard = KeyboardFactory(is_primary=True, user=self.user)

    def test_get_keyboard_anon(self):
        response = self.app.get(reverse('default-keyboard'))
        self.assertEqual(response.body, DEFAULT_KEYBOARD_STRING)

    def test_get_no_primary(self):
        user = UserFactory()
        response = self.app.get(reverse('default-keyboard'), user=user.username)
        self.assertEqual(DEFAULT_KEYBOARD_STRING, response.body)

    def test_get_primary_set(self):
        response = self.app.get(reverse('default-keyboard'), user=self.user.username)
        serializer = KeyboardSerializer(self.keyboard)
        self.assertEqual(JSONRenderer().render(serializer.data), response.body)


class KeyboardsListCreateAPITest(WebTest):
    fixtures = ['initial_data.json']
    csrf_checks = False

    def setUp(self):
        self.user = UserFactory()
        self.keyboard = KeyboardFactory(is_primary=True, user=self.user)

    def test_get_anon_empty(self):
        response = self.app.get(reverse('keyboards'))
        self.assertEqual(JSONRenderer().render([]), response.body)

    def test_get_user_kb_list(self):
        response = self.app.get(reverse('keyboards'), user=self.user)
        queryset = Keyboard.objects.filter(user=self.user)
        serializer = KeyboardOnlySerializer(queryset, many=True)
        self.assertEqual(JSONRenderer().render(serializer.data), response.body)

    def test_post_keyboard_logged_out(self):
        response = self.app.post(reverse('keyboards'), MOCK_KEYBOARD, status=403)
        self.assertEqual(response.status_code, 403)

    def test_post_keyboard_logged_in(self):
        response = self.app.post(reverse('keyboards'),
                                 json.dumps(MOCK_KEYBOARD),
                                 headers={'Content-Type': 'application/json'},
                                 user=self.user.username,
                                 status=201)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(Keyboard.objects.filter(user=self.user)), 2)

    def test_post_keyboard_missing_fields(self):
        response = self.app.post(reverse('keyboards'),
                                 json.dumps({k: v for k, v in
                                            MOCK_KEYBOARD.iteritems() if k != 'label'}),
                                 headers={'Content-Type': 'application/json'},
                                 user=self.user.username,
                                 status=400)
        self.assertEqual(response.body, '{"label": ["This field is required."]}')
        self.assertEqual(response.status_code, 400)

    def test_post_keyboard_missing_mappings(self):
        response = self.app.post(reverse('keyboards'),
                                 json.dumps({k: v for k, v in
                                            MOCK_KEYBOARD.iteritems() if k != 'mappings'}),
                                 headers={'Content-Type': 'application/json'},
                                 user=self.user.username,
                                 status=400)
        self.assertEqual('{"non_field_errors": ["Expected a list of items."]}', response.body)
        self.assertEqual(response.status_code, 400)


class KeyboardAPITest(WebTest):
    fixtures = ['initial_data.json']
    csrf_checks = False

    def setUp(self):
        self.user = UserFactory()
        self.keyboard = KeyboardFactory(is_primary=True, user=self.user)

    def test_get_keyboard_detail_anon(self):
        response = self.app.get(reverse('keyboard-detail',
                                        kwargs={'keyboard_id': self.keyboard.id}),
                                status=403)
        self.assertEqual(response.status_code, 403)

    def test_get_anothers_keyboard(self):
        user = UserFactory()
        response = self.app.get(reverse('keyboard-detail',
                                        kwargs={'keyboard_id': self.keyboard.id}),
                                user=user.username, status=403)
        self.assertEqual(response.status_code, 403)

    def get_own_keyboard_detail(self):
        response = self.app.get(reverse('keyboard-detail',
                                        kwargs={'keyboard_id': self.keyboard.id}),
                                user=self.user.username)
        serializer = KeyboardSerializer(self.keyboard)
        self.assertEqual(response.body, JSONRenderer().render(serializer.data))

    def get_nonexistent_keyboard_detail(self):
        response = self.app.get(reverse('keyboard-detail',
                                        kwargs={'keyboard_id': 99}),
                                user=self.user.username,
                                status=404)
        self.assertEqual(response.status_code, 404)

    def test_post_keyboard_detail_fails(self):
        response = self.app.post(reverse('keyboard-detail',
                                         kwargs={'keyboard_id': self.keyboard.id}),
                                 json.dumps(MOCK_KEYBOARD),
                                 headers={'Content-Type': 'application/json'},
                                 user=self.user.username,
                                 status=405)
        self.assertEqual(response.status_code, 405)

    def test_put_own_keyboard_logged_in(self):
        keyboard = KeyboardFactory(user=self.user, is_primary=False)
        response = self.app.put(reverse('keyboard-detail', kwargs={'keyboard_id': keyboard.id}),
                                json.dumps(MOCK_KEYBOARD),
                                headers={'Content-Type': 'application/json'},
                                user=self.user.username,
                                status=204)
        self.assertEqual(response.status_code, 204)

    def test_put_anothers_keyboard_logged_in(self):
        user = UserFactory()
        keyboard = KeyboardFactory(user=self.user, is_primary=False)
        response = self.app.put(reverse('keyboard-detail', kwargs={'keyboard_id': keyboard.id}),
                                json.dumps(MOCK_KEYBOARD),
                                headers={'Content-Type': 'application/json'},
                                user=user.username,
                                status=403)
        self.assertEqual(response.status_code, 403)

    def test_put_nonexistent_keyboard_logged_in(self):
        response = self.app.put(reverse('keyboard-detail', kwargs={'keyboard_id': 99}),
                                json.dumps(MOCK_KEYBOARD),
                                headers={'Content-Type': 'application/json'},
                                user=self.user.username,
                                status=404)
        self.assertEqual(response.status_code, 404)

    def test_put_keyboard_no_mappings(self):
        response = self.app.put(reverse('keyboard-detail', kwargs={'keyboard_id': self.keyboard.id}),
                                json.dumps({k: v for k, v in
                                            MOCK_KEYBOARD.iteritems() if k != 'mappings'}),
                                headers={'Content-Type': 'application/json'},
                                user=self.user.username,
                                status=400)
        self.assertEqual('{"non_field_errors": ["Expected a list of items."]}', response.body)
        self.assertEqual(response.status_code, 400)

    def test_put_keyboard_missing_fields(self):
        response = self.app.put(reverse('keyboard-detail', kwargs={'keyboard_id': self.keyboard.id}),
                                json.dumps({k: v for k, v in
                                            MOCK_KEYBOARD.iteritems() if k != 'label'}),
                                headers={'Content-Type': 'application/json'},
                                user=self.user.username,
                                status=400)
        self.assertEqual(response.body, '{"label": ["This field is required."]}')
        self.assertEqual(response.status_code, 400)

    def test_put_keyboard_logged_out(self):
        response = self.app.put(reverse('keyboard-detail', kwargs={'keyboard_id': self.keyboard.id}),
                                json.dumps(MOCK_KEYBOARD),
                                headers={'Content-Type': 'application/json'},
                                status=403)
        self.assertEqual(response.status_code, 403)

    def test_delete_keyboard_logged_out(self):
        response = self.app.delete(reverse('keyboard-detail',
                                           kwargs={'keyboard_id': self.keyboard.id}),
                                   status=403)
        self.assertEqual(response.status_code, 403)

    def test_delete_keyboard_not_exists(self):
        response = self.app.delete(reverse('keyboard-detail',
                                           kwargs={'keyboard_id': 99}),
                                   user=self.user.username,
                                   status=204)
        self.assertEqual(response.status_code, 204)

    def test_delete_anothers_keyboard(self):
        user = UserFactory()
        response = self.app.delete(reverse('keyboard-detail',
                                           kwargs={'keyboard_id': self.keyboard.id}),
                                   user=user.username,
                                   status=403)
        self.assertEqual(response.status_code, 403)

    def test_delete_keyboard_exists(self):
        response = self.app.delete(reverse('keyboard-detail',
                                           kwargs={'keyboard_id': self.keyboard.id}),
                                   user=self.user.username,
                                   status=204)
        self.assertEqual(response.status_code, 204)
        with self.assertRaises(Keyboard.DoesNotExist):
            Keyboard.objects.get(id=self.keyboard.id)


class TestKeyMapSerializer(TestCase):
    fixtures = ['initial_data.json']

    def get_cell(self, id):
        return CellType.objects.get(id=id)

    def setUp(self):
        self.single_keymap = {'cellid': 1, 'key': 'a'}
        self.keymap_list = [{'cellid': 1, 'key': 'a'},
                            {'cellid': 2, 'key': 'b'},
                            {'cellid': 3, 'key': 'c'},
                            {'cellid': 4, 'key': 'd'}]

    def test_save_one(self):
        old_maps = len(KeyMap.objects.all())
        serializer = KeyMapSerializer(data=self.single_keymap)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.assertEqual(len(KeyMap.objects.all()), old_maps+1)

    def test_save_many(self):
        old_maps = len(KeyMap.objects.all())
        serializer = KeyMapSerializer(data=self.keymap_list, many=True)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.assertEqual(len(KeyMap.objects.all()), old_maps+4)

    def test_save_one_exists(self):
        keymap = KeyMapFactory(cellid=self.get_cell(1), key='a')
        old_maps = len(KeyMap.objects.all())
        serializer = KeyMapSerializer(data=self.single_keymap)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.assertEqual(keymap, serializer.object)
        self.assertEqual(old_maps, len(KeyMap.objects.all()))

    def test_save_many_some_exist(self):
        keymap1 = KeyMapFactory(cellid=self.get_cell(1), key='a')
        keymap2 = KeyMapFactory(cellid=self.get_cell(2), key='b')
        old_maps = len(KeyMap.objects.all())
        serializer = KeyMapSerializer(data=self.keymap_list, many=True)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.assertEqual(len(KeyMap.objects.all()), old_maps+2)
        map_list = []
        for mapping in serializer.object:
            map_list.append(mapping)
        self.assertIn(keymap1, map_list)
        self.assertIn(keymap2, map_list)