import json

from django_webtest import WebTest
from django.test import TestCase

from django.urls import reverse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from cellcounter.main.models import CellType
from .defaults import MOCK_KEYBOARD, MOCK_KEYBOARD2, BAD_KEYBOARD
from .defaults import BUILTIN_KEYBOARD_STRING, BUILTIN_KEYBOARD_STRING_LOGGED_IN
from .defaults import BUILTIN_DESKTOP_KEYBOARD_MAP, BUILTIN_MOBILE_KEYBOARD_MAP
from .factories import (
    UserFactory,
    KeyboardFactory,
    KeyMapFactory,
    DefaultKeyboardFactory,
    DefaultKeyboardsFactory,
    BuiltinKeyboardFactory,
)
from .models import Keyboard, DefaultKeyboards
from .serializers import KeyboardSerializer, KeyboardListItemSerializer

from io import StringIO

from datetime import datetime
import pytz


def DecodeDateTimeInUTC(d, fields=["created", "last_modified"]):
    """Utility function to convert datetime fields to UTC"""

    def to_utc(datetime_string):
        return datetime.fromisoformat(
            datetime_string.replace("Z", "+00:00")
        ).astimezone(pytz.utc)

    for f in fields:
        if f in d:
            d[f] = to_utc(d[f])
    return d


class KeyboardTestCase(TestCase):
    def test_unicode(self):
        keyboard = KeyboardFactory(user__username="alpha", label="alpha")
        self.assertEqual(keyboard.__unicode__(), "Keyboard 'alpha' for user 'alpha'")

    def test_set_keymaps(self):
        user = UserFactory()
        keyboard = KeyboardFactory(user=user)
        number_old_maps = len(keyboard.mappings.all())
        new_maps = [KeyMapFactory(cellid=CellType.objects.get(id=1))]
        keyboard.set_keymaps(new_maps)

        self.assertNotEqual(number_old_maps, len(keyboard.mappings.all()))
        self.assertEqual(len(new_maps), len(keyboard.mappings.all()))


class KeyboardsAPIListTest(WebTest):
    csrf_checks = False

    def setUp(self):
        self.user = UserFactory()
        self.desktop_keyboard = KeyboardFactory(
            user=self.user, device_type=Keyboard.DESKTOP
        )
        self.mobile_keyboard = KeyboardFactory(
            user=self.user, device_type=Keyboard.MOBILE
        )
        self.builtin_desktop_keyboard = BuiltinKeyboardFactory(
            device_type=Keyboard.DESKTOP
        )
        self.builtin_mobile_keyboard = BuiltinKeyboardFactory(
            device_type=Keyboard.MOBILE
        )

        self.maxDiff = None

    def test_get_keyboard_default_anon(self):
        response = self.app.get(reverse("keyboards-list"))

        # decode the datetime fields in UTC for comparison (app is timezone aware)
        a = json.loads(BUILTIN_KEYBOARD_STRING, object_hook=DecodeDateTimeInUTC)
        b = json.loads(response.body.decode("utf-8"), object_hook=DecodeDateTimeInUTC)
        self.assertEqual(a, b)

    def test_get_keyboard_default_logged_in(self):
        # create a default user with no keyboards
        self.maxDiff = None
        user = UserFactory(username="test")
        response = self.app.get(reverse("keyboards-list"), user=user.username)

        # decode the datetime fields in UTC for comparison (app is timezone aware)
        a = json.loads(
            BUILTIN_KEYBOARD_STRING_LOGGED_IN, object_hook=DecodeDateTimeInUTC
        )
        b = json.loads(response.body.decode("utf-8"), object_hook=DecodeDateTimeInUTC)
        self.assertEqual(a, b)

    def test_get_default_notset(self):
        # use a user but don't have any default keyboard set
        response = self.app.get(reverse("keyboards-list"), user=self.user.username)

        # XXX: the default is currently set in the view, so mirror that in the test
        self.builtin_desktop_keyboard.set_default()
        self.builtin_mobile_keyboard.set_default()

        keyboards = [
            self.builtin_desktop_keyboard,
            self.builtin_mobile_keyboard,
            self.desktop_keyboard,
            self.mobile_keyboard,
        ]
        serializer = []
        for kb in keyboards:
            serializer.append(kb.serialize(many=True))
        # serializer = KeyboardListItemSerializer(keyboards, many=True)
        self.assertEqual(JSONRenderer().render(serializer), response.body)
        self.assertEqual(serializer[0]["is_default"], True)
        self.assertEqual(serializer[1]["is_default"], True)
        self.assertEqual(serializer[2]["is_default"], False)
        self.assertEqual(serializer[3]["is_default"], False)

    def test_get_default_set(self):
        # use a user with a default desktop and user keyboard
        if not hasattr(self.user, "defaultkeyboards"):
            self.user.defaultkeyboards = DefaultKeyboards.objects.create(user=self.user)
        self.user.defaultkeyboards.desktop = self.desktop_keyboard
        self.user.defaultkeyboards.mobile = self.mobile_keyboard
        self.user.defaultkeyboards.save()

        response = self.app.get(reverse("keyboards-list"), user=self.user.username)

        # XXX: the default is currently set in the view, so mirror that in the test
        self.desktop_keyboard.set_default()
        self.mobile_keyboard.set_default()

        keyboards = [
            self.builtin_desktop_keyboard,
            self.builtin_mobile_keyboard,
            self.desktop_keyboard,
            self.mobile_keyboard,
        ]
        serializer = []
        for kb in keyboards:
            serializer.append(kb.serialize(many=True))
        self.assertEqual(JSONRenderer().render(serializer), response.body)
        self.assertEqual(serializer[0]["is_default"], False)
        self.assertEqual(serializer[1]["is_default"], False)
        self.assertEqual(serializer[2]["is_default"], True)
        self.assertEqual(serializer[3]["is_default"], True)

    # test put
    def test_put_keyboard_logged_out(self):
        response = self.app.put(reverse("keyboards-list"), MOCK_KEYBOARD, status=403)
        self.assertEqual(response.status_code, 403)

    def test_put_keyboard_list(self):
        response = self.app.put(
            reverse("keyboards-list"), MOCK_KEYBOARD, user=self.user, status=405
        )
        self.assertEqual(response.status_code, 405)

    # test delete
    def test_delete_keyboard_logged_out(self):
        response = self.app.delete(reverse("keyboards-list"), status=403)
        self.assertEqual(response.status_code, 403)

    def test_delete_keyboard_list(self):
        response = self.app.delete(
            reverse("keyboards-list"), user=self.user, status=405
        )
        self.assertEqual(response.status_code, 405)

    # test post
    def test_post_keyboard_logged_out(self):
        response = self.app.post(reverse("keyboards-list"), MOCK_KEYBOARD, status=403)
        self.assertEqual(response.status_code, 403)

    def test_post_keyboard_list(self):
        response = self.app.post(
            reverse("keyboards-list"), MOCK_KEYBOARD, user=self.user, status=405
        )
        self.assertEqual(response.status_code, 405)


class KeyboardsAPIDesktopListTest(WebTest):
    csrf_checks = False

    def setUp(self):
        self.user = UserFactory()
        self.desktop_keyboard = KeyboardFactory(
            user=self.user, device_type=Keyboard.DESKTOP
        )
        self.mobile_keyboard = KeyboardFactory(
            user=self.user, device_type=Keyboard.MOBILE
        )
        self.builtin_desktop_keyboard = BuiltinKeyboardFactory(
            device_type=Keyboard.DESKTOP
        )
        self.builtin_mobile_keyboard = BuiltinKeyboardFactory(
            device_type=Keyboard.MOBILE
        )

    # test get
    def test_get_keyboard_desktop_builtin(self):
        response = self.app.get(
            reverse("keyboards-desktop-list"), user=self.user, status=200
        )

        # XXX: the default is currently set in the view, so mirror that in the test
        self.builtin_desktop_keyboard.set_default()

        keyboards = [self.builtin_desktop_keyboard, self.desktop_keyboard]
        serializer = []
        for kb in keyboards:
            serializer.append(kb.serialize(many=True))
        self.assertEqual(JSONRenderer().render(serializer), response.body)

    def test_get_keyboard_desktop_builtin_logged_out(self):
        response = self.app.get(reverse("keyboards-desktop-list"), status=200)

        # XXX: the default is currently set in the view, so mirror that in the test
        self.builtin_desktop_keyboard.set_default()

        serializer = [self.builtin_desktop_keyboard.serialize(many=True)]
        self.assertEqual(JSONRenderer().render(serializer), response.body)

    # test put
    def test_put_keyboard_logged_out(self):
        response = self.app.put(
            reverse("keyboards-desktop-list"), MOCK_KEYBOARD, status=403
        )
        self.assertEqual(response.status_code, 403)

    def test_put_keyboard(self):
        response = self.app.put(
            reverse("keyboards-desktop-list"), MOCK_KEYBOARD, user=self.user, status=405
        )
        self.assertEqual(response.status_code, 405)

    # test delete
    def test_delete_keyboard_logged_out(self):
        response = self.app.delete(reverse("keyboards-desktop-list"), status=403)
        self.assertEqual(response.status_code, 403)

    def test_delete_keyboard(self):
        response = self.app.delete(
            reverse("keyboards-desktop-list"), user=self.user, status=405
        )
        self.assertEqual(response.status_code, 405)

    # test post
    def test_post_keyboard_logged_out(self):
        response = self.app.post(
            reverse("keyboards-desktop-list"), MOCK_KEYBOARD, status=403
        )
        self.assertEqual(response.status_code, 403)

    def test_post_keyboard_logged_in(self):
        response = self.app.post(
            reverse("keyboards-desktop-list"),
            json.dumps(MOCK_KEYBOARD),
            headers={"Content-Type": "application/json"},
            user=self.user.username,
            status=201,
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(Keyboard.objects.filter(user=self.user)), 3)

    def test_post_keyboard_missing_fields(self):
        response = self.app.post(
            reverse("keyboards-desktop-list"),
            json.dumps({k: v for k, v in list(MOCK_KEYBOARD.items()) if k != "label"}),
            headers={"Content-Type": "application/json"},
            user=self.user.username,
            status=400,
        )
        self.assertEqual(
            response.body.decode("utf-8"), '{"label":["This field is required."]}'
        )
        self.assertEqual(response.status_code, 400)

    def test_post_keyboard_missing_mappings(self):
        response = self.app.post(
            reverse("keyboards-desktop-list"),
            json.dumps(
                {k: v for k, v in list(MOCK_KEYBOARD.items()) if k != "mappings"}
            ),
            headers={"Content-Type": "application/json"},
            user=self.user.username,
            status=400,
        )
        self.assertEqual(
            '{"mappings":["This field is required."]}', response.body.decode("utf-8")
        )
        self.assertEqual(response.status_code, 400)


class KeyboardsAPIDesktopDetailTest(WebTest):
    csrf_checks = False

    def setUp(self):
        self.user = UserFactory()
        self.desktop_keyboard = KeyboardFactory(
            user=self.user, device_type=Keyboard.DESKTOP
        )
        self.mobile_keyboard = KeyboardFactory(
            user=self.user, device_type=Keyboard.MOBILE
        )
        self.builtin_desktop_keyboard = BuiltinKeyboardFactory(
            device_type=Keyboard.DESKTOP
        )
        self.builtin_mobile_keyboard = BuiltinKeyboardFactory(
            device_type=Keyboard.MOBILE
        )

    ##### test get
    def test_get_keyboard_desktop_builtin(self):
        response = self.app.get(
            reverse("keyboards-desktop-detail", kwargs={"pk": "builtin"}),
            user=self.user,
            status=200,
        )
        serializer = self.builtin_desktop_keyboard.serialize()
        self.assertEqual(JSONRenderer().render(serializer), response.body)

    def test_get_keyboard_desktop_builtin_logged_out(self):
        response = self.app.get(
            reverse("keyboards-desktop-detail", kwargs={"pk": "builtin"}), status=200
        )
        serializer = self.builtin_desktop_keyboard.serialize()
        self.assertEqual(JSONRenderer().render(serializer), response.body)

    def test_get_keyboard_desktop_default(self):
        response = self.app.get(
            reverse("keyboards-desktop-detail", kwargs={"pk": "default"}),
            user=self.user,
            status=200,
        )
        serializer = self.builtin_desktop_keyboard.serialize()
        self.assertEqual(JSONRenderer().render(serializer), response.body)

    def test_get_keyboard_desktop_default_logged_out(self):
        response = self.app.get(
            reverse("keyboards-desktop-detail", kwargs={"pk": "default"}), status=200
        )
        serializer = self.builtin_desktop_keyboard.serialize()
        self.assertEqual(JSONRenderer().render(serializer), response.body)

    def test_get_keyboard_desktop_anothers_keyboard(self):
        user = UserFactory()
        response = self.app.get(
            reverse(
                "keyboards-desktop-detail", kwargs={"pk": self.desktop_keyboard.id}
            ),
            user=user.username,
            status=404,
        )
        self.assertEqual(response.status_code, 404)

    def test_get_keyboard_desktop_keyboard(self):
        response = self.app.get(
            reverse(
                "keyboards-desktop-detail", kwargs={"pk": self.desktop_keyboard.id}
            ),
            user=self.user,
            status=200,
        )
        serializer = KeyboardSerializer(self.desktop_keyboard)
        self.assertEqual(JSONRenderer().render(serializer.data), response.body)

    def test_get_keyboard_desktop_keyboard_mobile(self):
        response = self.app.get(
            reverse("keyboards-mobile-detail", kwargs={"pk": self.desktop_keyboard.id}),
            user=self.user,
            status=404,
        )
        self.assertEqual(response.status_code, 404)

    def test_get_keyboard_desktop_keyboard_logged_out(self):
        response = self.app.get(
            reverse(
                "keyboards-desktop-detail", kwargs={"pk": self.desktop_keyboard.id}
            ),
            status=404,
        )
        self.assertEqual(response.status_code, 404)

    def test_get_desktop_nonexistent_keyboard_detail(self):
        response = self.app.get(
            reverse("keyboards-desktop-detail", kwargs={"pk": 99}),
            user=self.user.username,
            status=404,
        )
        self.assertEqual(response.status_code, 404)

    ##### test put
    def test_put_keyboard_desktop_logged_out(self):
        response = self.app.put(
            reverse("keyboards-desktop-detail", kwargs={"pk": "builtin"}),
            MOCK_KEYBOARD,
            status=403,
        )
        self.assertEqual(response.status_code, 403)

    def test_put_keyboard_desktop_builtin(self):
        response = self.app.put(
            reverse("keyboards-desktop-detail", kwargs={"pk": "builtin"}),
            MOCK_KEYBOARD,
            user=self.user.username,
            status=400,
        )
        self.assertEqual(response.status_code, 400)

    def test_put_keyboard_desktop_no_data(self):
        response = self.app.put(
            reverse(
                "keyboards-desktop-detail", kwargs={"pk": self.desktop_keyboard.id}
            ),
            user=self.user.username,
            status=400,
        )
        self.assertEqual(
            '{"label":["This field is required."],"device_type":["This field is required."],"mappings":["This field is required."]}',
            response.body.decode("utf-8"),
        )
        self.assertEqual(response.status_code, 400)

    def test_put_keyboard_desktop_invalid_data(self):
        response = self.app.put(
            reverse(
                "keyboards-desktop-detail", kwargs={"pk": self.desktop_keyboard.id}
            ),
            BAD_KEYBOARD,
            user=self.user.username,
            status=400,
        )
        self.assertEqual(
            '{"label":["This field is required."],"device_type":["\\"desktopz\\" is not a valid choice."],"mappings":["This field is required."]}',
            response.body.decode("utf-8"),
        )
        self.assertEqual(response.status_code, 400)

    def test_put_keyboard_desktop_nonexistent_keyboard_logged_in(self):
        response = self.app.put(
            reverse("keyboards-desktop-detail", kwargs={"pk": 99}),
            json.dumps(MOCK_KEYBOARD),
            headers={"Content-Type": "application/json"},
            user=self.user.username,
            status=404,
        )
        self.assertEqual(response.status_code, 404)

    def test_put_keyboard_desktop_no_mappings(self):
        response = self.app.put(
            reverse(
                "keyboards-desktop-detail", kwargs={"pk": self.desktop_keyboard.id}
            ),
            json.dumps({k: v for k, v in MOCK_KEYBOARD.items() if k != "mappings"}),
            headers={"Content-Type": "application/json"},
            user=self.user.username,
            status=400,
        )
        self.assertEqual(
            '{"mappings":["This field is required."]}', response.body.decode("utf-8")
        )
        self.assertEqual(response.status_code, 400)

    def test_put_keyboard_desktop_missing_fields(self):
        response = self.app.put(
            reverse(
                "keyboards-desktop-detail", kwargs={"pk": self.desktop_keyboard.id}
            ),
            json.dumps({k: v for k, v in MOCK_KEYBOARD.items() if k != "label"}),
            headers={"Content-Type": "application/json"},
            user=self.user.username,
            status=400,
        )
        self.assertEqual(
            response.body.decode("utf-8"), '{"label":["This field is required."]}'
        )
        self.assertEqual(response.status_code, 400)

    def test_put_keyboard_desktop_valid_data(self):
        # response = self.client.put(reverse('keyboards-desktop-detail', kwargs={'pk': self.desktop_keyboard.id}), MOCK_KEYBOARD2, user=self.user.username, content_type='application/json')
        response = self.app.put_json(
            reverse(
                "keyboards-desktop-detail", kwargs={"pk": self.desktop_keyboard.id}
            ),
            MOCK_KEYBOARD2,
            user=self.user.username,
        )
        response = self.app.get(
            reverse(
                "keyboards-desktop-detail", kwargs={"pk": self.desktop_keyboard.id}
            ),
            user=self.user,
            status=200,
        )
        a = json.loads(response.body.decode("utf-8"))
        self.assertEqual(a["id"], self.desktop_keyboard.id)
        self.assertEqual(a["label"], "Keyboard2")
        self.assertEqual(response.status_code, 200)

    ##### test delete
    def test_delete_keyboard_logged_out(self):
        response = self.app.delete(
            reverse(
                "keyboards-desktop-detail", kwargs={"pk": self.desktop_keyboard.id}
            ),
            status=403,
        )
        self.assertEqual(response.status_code, 403)

    def test_delete_keyboard_builtin(self):
        response = self.app.delete(
            reverse("keyboards-desktop-detail", kwargs={"pk": "builtin"}),
            user=self.user,
            status=400,
        )
        self.assertEqual(response.status_code, 400)

    def test_delete_keyboard_desktop(self):
        self.assertEqual(len(Keyboard.objects.filter(user=self.user)), 2)
        response = self.app.delete(
            reverse(
                "keyboards-desktop-detail", kwargs={"pk": self.desktop_keyboard.id}
            ),
            user=self.user,
            status=200,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(Keyboard.objects.filter(user=self.user)), 1)
        with self.assertRaises(Keyboard.DoesNotExist):
            Keyboard.objects.get(id=self.desktop_keyboard.id)

    def test_delete_keyboard_desktop_mobile(self):
        self.assertEqual(len(Keyboard.objects.filter(user=self.user)), 2)
        response = self.app.delete(
            reverse("keyboards-desktop-detail", kwargs={"pk": self.mobile_keyboard.id}),
            user=self.user,
            status=404,
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(len(Keyboard.objects.filter(user=self.user)), 2)

    def test_delete_keyboard_desktop_other_user(self):
        user = UserFactory()
        self.assertEqual(len(Keyboard.objects.filter(user=self.user)), 2)
        response = self.app.delete(
            reverse("keyboards-desktop-detail", kwargs={"pk": self.mobile_keyboard.id}),
            user=user,
            status=404,
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(len(Keyboard.objects.filter(user=self.user)), 2)
        self.assertEqual(
            '{"detail":"desktop keyboard with id \''
            + str(self.mobile_keyboard.id)
            + "' not found\"}",
            response.body.decode("utf-8"),
        )

    ##### test post
    def test_post_keyboard_desktop_logged_out(self):
        response = self.app.post(
            reverse("keyboards-desktop-detail", kwargs={"pk": "builtin"}),
            MOCK_KEYBOARD,
            status=403,
        )
        self.assertEqual(response.status_code, 403)

    def test_post_keyboard_desktop_no_post(self):
        response = self.app.post(
            reverse("keyboards-desktop-detail", kwargs={"pk": "builtin"}),
            MOCK_KEYBOARD,
            user=self.user.username,
            status=405,
        )
        self.assertEqual(response.status_code, 405)


class KeyboardsAPIDesktopSetDefaultTest(WebTest):
    csrf_checks = False

    def setUp(self):
        self.user = UserFactory()
        self.desktop_keyboard = KeyboardFactory(
            user=self.user, device_type=Keyboard.DESKTOP
        )
        self.mobile_keyboard = KeyboardFactory(
            user=self.user, device_type=Keyboard.MOBILE
        )
        self.builtin_desktop_keyboard = BuiltinKeyboardFactory(
            device_type=Keyboard.DESKTOP
        )
        self.builtin_mobile_keyboard = BuiltinKeyboardFactory(
            device_type=Keyboard.MOBILE
        )

    ##### test get
    def test_get_keyboard_logged_out(self):
        response = self.app.get(
            reverse("keyboards-desktop-set_default", kwargs={"pk": "builtin"}),
            MOCK_KEYBOARD,
            status=405,
        )
        self.assertEqual(response.status_code, 405)

    def test_get_keyboard(self):
        response = self.app.get(
            reverse("keyboards-desktop-set_default", kwargs={"pk": "builtin"}),
            MOCK_KEYBOARD,
            user=self.user,
            status=405,
        )
        self.assertEqual(response.status_code, 405)

    ##### test post
    def test_post_keyboard_logged_out(self):
        response = self.app.post(
            reverse("keyboards-desktop-set_default", kwargs={"pk": "builtin"}),
            MOCK_KEYBOARD,
            status=403,
        )
        self.assertEqual(response.status_code, 403)

    def test_post_keyboard(self):
        response = self.app.post(
            reverse("keyboards-desktop-set_default", kwargs={"pk": "builtin"}),
            MOCK_KEYBOARD,
            user=self.user,
            status=405,
        )
        self.assertEqual(response.status_code, 405)

    ##### test delete
    def test_delete_keyboard_logged_out(self):
        response = self.app.delete(
            reverse("keyboards-desktop-set_default", kwargs={"pk": "builtin"}),
            status=403,
        )
        self.assertEqual(response.status_code, 403)

    def test_delete_keyboard(self):
        response = self.app.delete(
            reverse("keyboards-desktop-set_default", kwargs={"pk": "builtin"}),
            user=self.user,
            status=405,
        )
        self.assertEqual(response.status_code, 405)

    ##### test put
    def test_put_keyboard_desktop_logged_out(self):
        response = self.app.put(
            reverse("keyboards-desktop-set_default", kwargs={"pk": "builtin"}),
            MOCK_KEYBOARD,
            status=403,
        )
        self.assertEqual(response.status_code, 403)

    def test_put_keyboard_desktop_builtin_default(self):
        response = self.app.put(
            reverse("keyboards-desktop-set_default", kwargs={"pk": "builtin"}),
            user=self.user.username,
            status=200,
        )
        self.assertEqual('{"status":"Default cleared"}', response.body.decode("utf-8"))
        self.assertEqual(response.status_code, 200)

    def test_put_keyboard_desktop_set_user_default(self):
        # retrieve the default keyboard
        response = self.app.get(
            reverse("keyboards-desktop-detail", kwargs={"pk": "default"}),
            user=self.user,
            status=200,
        )
        # assert that it is the builtin keyboard
        serializer = self.builtin_desktop_keyboard.serialize()
        self.assertEqual(JSONRenderer().render(serializer), response.body)
        response = self.app.put(
            reverse(
                "keyboards-desktop-set_default", kwargs={"pk": self.desktop_keyboard.id}
            ),
            user=self.user.username,
            status=200,
        )
        self.assertEqual(response.status_code, 200)

        # retrieve the new default keyboard
        response = self.app.get(
            reverse("keyboards-desktop-detail", kwargs={"pk": "default"}),
            user=self.user,
            status=200,
        )
        # assert that it is the user's keyboard
        serializer = KeyboardSerializer(self.desktop_keyboard)
        self.assertEqual(JSONRenderer().render(serializer.data), response.body)

    def test_put_keyboard_desktop_mobile(self):
        response = self.app.put(
            reverse(
                "keyboards-desktop-set_default", kwargs={"pk": self.mobile_keyboard.id}
            ),
            MOCK_KEYBOARD,
            user=self.user.username,
            status=404,
        )
        self.assertEqual(response.status_code, 404)


class KeyboardsAPIMobileDetailTest(WebTest):
    csrf_checks = False

    def setUp(self):
        self.user = UserFactory()
        self.desktop_keyboard = KeyboardFactory(
            user=self.user, device_type=Keyboard.DESKTOP
        )
        self.mobile_keyboard = KeyboardFactory(
            user=self.user, device_type=Keyboard.MOBILE
        )
        self.builtin_desktop_keyboard = BuiltinKeyboardFactory(
            device_type=Keyboard.DESKTOP
        )
        self.builtin_mobile_keyboard = BuiltinKeyboardFactory(
            device_type=Keyboard.MOBILE
        )

    # test get
    def test_get_keyboard_mobile_builtin(self):
        response = self.app.get(
            reverse("keyboards-mobile-detail", kwargs={"pk": "builtin"}), status=200
        )
        self.assertEqual(
            JSONRenderer().render(self.builtin_mobile_keyboard.serialize()),
            response.body,
        )

    def test_get_keyboard_mobile_default(self):
        response = self.app.get(
            reverse("keyboards-mobile-detail", kwargs={"pk": "default"}), status=200
        )
        self.assertEqual(
            JSONRenderer().render(self.builtin_mobile_keyboard.serialize()),
            response.body,
        )

    def test_get_keyboard_mobile_default_logged_in(self):
        response = self.app.get(
            reverse("keyboards-mobile-detail", kwargs={"pk": "default"}),
            user=self.user,
            status=200,
        )
        self.assertEqual(
            JSONRenderer().render(self.builtin_mobile_keyboard.serialize()),
            response.body,
        )

    def test_get_keyboard_mobile_keyboard(self):
        response = self.app.get(
            reverse("keyboards-mobile-detail", kwargs={"pk": self.mobile_keyboard.id}),
            user=self.user,
            status=200,
        )
        serializer = KeyboardSerializer(self.mobile_keyboard)
        self.assertEqual(JSONRenderer().render(serializer.data), response.body)

    def test_get_keyboard_mobile_keyboard_desktop(self):
        response = self.app.get(
            reverse("keyboards-desktop-detail", kwargs={"pk": self.mobile_keyboard.id}),
            user=self.user,
            status=404,
        )
        self.assertEqual(response.status_code, 404)

    def test_get_keyboard_mobile_keyboard_logged_out(self):
        response = self.app.get(
            reverse("keyboards-mobile-detail", kwargs={"pk": self.mobile_keyboard.id}),
            status=404,
        )
        self.assertEqual(response.status_code, 404)

    # test put
    # test delete

    def test_post_keyboard_desktop_logged_out(self):
        response = self.app.post(
            reverse("keyboards-desktop-detail", kwargs={"pk": "builtin"}),
            MOCK_KEYBOARD,
            status=403,
        )
        self.assertEqual(response.status_code, 403)

    def test_post_keyboard_mobile_logged_out(self):
        response = self.app.post(
            reverse("keyboards-mobile-detail", kwargs={"pk": "builtin"}),
            MOCK_KEYBOARD,
            status=403,
        )
        self.assertEqual(response.status_code, 403)

    def test_post_keyboard_desktop_no_post(self):
        response = self.app.post(
            reverse("keyboards-desktop-detail", kwargs={"pk": "builtin"}),
            MOCK_KEYBOARD,
            user=self.user.username,
            status=405,
        )
        self.assertEqual(response.status_code, 405)

    def test_post_keyboard_mobile_no_post(self):
        response = self.app.post(
            reverse("keyboards-mobile-detail", kwargs={"pk": "builtin"}),
            MOCK_KEYBOARD,
            user=self.user.username,
            status=405,
        )
        self.assertEqual(response.status_code, 405)

    # test post
    def test_post_keyboard_mobile_logged_out(self):
        response = self.app.post(
            reverse("keyboards-mobile-detail", kwargs={"pk": "builtin"}),
            MOCK_KEYBOARD,
            status=403,
        )
        self.assertEqual(response.status_code, 403)

    def test_post_keyboard_mobile_no_post(self):
        response = self.app.post(
            reverse("keyboards-mobile-detail", kwargs={"pk": "builtin"}),
            MOCK_KEYBOARD,
            user=self.user.username,
            status=405,
        )
        self.assertEqual(response.status_code, 405)


class KeyboardsAPICompositeActions(WebTest):
    csrf_checks = False

    def setUp(self):
        self.user = UserFactory()
        self.desktop_keyboard = KeyboardFactory(
            user=self.user, device_type=Keyboard.DESKTOP
        )
        self.mobile_keyboard = KeyboardFactory(
            user=self.user, device_type=Keyboard.MOBILE
        )
        self.builtin_desktop_keyboard = BuiltinKeyboardFactory(
            device_type=Keyboard.DESKTOP
        )
        self.builtin_mobile_keyboard = BuiltinKeyboardFactory(
            device_type=Keyboard.MOBILE
        )

    def test_keyboard_desktop_mobile_set_user_default(self):
        # retrieve the default desktop keyboard
        response = self.app.get(
            reverse("keyboards-desktop-detail", kwargs={"pk": "default"}),
            user=self.user,
            status=200,
        )
        # assert that it is the builtin keyboard
        serializer = self.builtin_desktop_keyboard.serialize()
        self.assertEqual(JSONRenderer().render(serializer), response.body)

        # retrieve the default mobile keyboard
        response = self.app.get(
            reverse("keyboards-mobile-detail", kwargs={"pk": "default"}),
            user=self.user,
            status=200,
        )
        # assert that it is the builtin mobile keyboard
        serializer = self.builtin_mobile_keyboard.serialize()
        self.assertEqual(JSONRenderer().render(serializer), response.body)

        # set the default desktop keyboard...
        response = self.app.put(
            reverse(
                "keyboards-desktop-set_default", kwargs={"pk": self.desktop_keyboard.id}
            ),
            user=self.user.username,
            status=200,
        )
        self.assertEqual(response.status_code, 200)

        # ... and the mobile one
        response = self.app.put(
            reverse(
                "keyboards-mobile-set_default", kwargs={"pk": self.mobile_keyboard.id}
            ),
            user=self.user.username,
            status=200,
        )
        self.assertEqual(response.status_code, 200)

        # retrieve the new default desktop keyboard
        response = self.app.get(
            reverse("keyboards-desktop-detail", kwargs={"pk": "default"}),
            user=self.user,
            status=200,
        )
        # assert that it is the user's keyboard
        serializer = self.desktop_keyboard.serialize()
        self.assertEqual(JSONRenderer().render(serializer), response.body)

        # retrieve the new default mobile keyboard
        response = self.app.get(
            reverse("keyboards-mobile-detail", kwargs={"pk": "default"}),
            user=self.user,
            status=200,
        )
        # assert that it is the user's keyboard
        serializer = self.mobile_keyboard.serialize()
        self.assertEqual(JSONRenderer().render(serializer), response.body)

        # delete the desktop keyboard
        response = self.app.delete(
            reverse(
                "keyboards-desktop-detail", kwargs={"pk": self.desktop_keyboard.id}
            ),
            user=self.user,
            status=200,
        )
        self.assertEqual(response.status_code, 200)

        # retrieve the new default desktop keyboard
        response = self.app.get(
            reverse("keyboards-desktop-detail", kwargs={"pk": "default"}),
            user=self.user,
            status=200,
        )
        # assert that it is the builtin keyboard
        serializer = self.builtin_desktop_keyboard.serialize()
        self.assertEqual(JSONRenderer().render(serializer), response.body)

        # retrieve the new default mobile keyboard
        response = self.app.get(
            reverse("keyboards-mobile-detail", kwargs={"pk": "default"}),
            user=self.user,
            status=200,
        )
        # assert that it is the user's keyboard
        serializer = self.mobile_keyboard.serialize()
        self.assertEqual(JSONRenderer().render(serializer), response.body)
