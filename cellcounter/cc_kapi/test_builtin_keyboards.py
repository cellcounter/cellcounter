import json

from django.test import TestCase

# from .factories import KeyboardLayoutsFactory
from .marshalls import KeyboardLayoutsMarshall
from .factories import UserFactory, KeyboardFactory, BuiltinKeyboardFactory
from .models import Keyboard


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


class KeyboardLayoutsTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.desktop_keyboard = KeyboardFactory(
            user=self.user, device_type=Keyboard.DESKTOP
        )
        self.mobile_keyboard = KeyboardFactory(
            user=self.user, device_type=Keyboard.MOBILE
        )

    def test_builtin_keyboard_factory(self):
        """Check that the builtin keyboard factory returns the same keyboards as the marshall."""

        builtin_desktop_keyboard_factory = BuiltinKeyboardFactory(
            device_type=Keyboard.DESKTOP
        )
        builtin_mobile_keyboard_factory = BuiltinKeyboardFactory(
            device_type=Keyboard.MOBILE
        )
        [
            builtin_desktop_keyboard_marshall,
            builtin_mobile_keyboard_marshall,
        ] = KeyboardLayoutsMarshall().get_all(layout_types="builtin")
        self.assertEqual(
            builtin_desktop_keyboard_factory.serialize(),
            builtin_desktop_keyboard_marshall.serialize(),
        )
        self.assertEqual(
            builtin_mobile_keyboard_factory.serialize(),
            builtin_mobile_keyboard_marshall.serialize(),
        )

    def test_builtin_keyboards_count(self):
        builtin_keyboards = KeyboardLayoutsMarshall().get_all(layout_types="builtin")
        self.assertEqual(len(builtin_keyboards), 2)
        self.assertEqual(builtin_keyboards[0].layout_type(), "builtin")
        self.assertEqual(builtin_keyboards[1].layout_type(), "builtin")

        builtin_keyboard_desktop = KeyboardLayoutsMarshall().get_all(
            layout_types="builtin", device=Keyboard.DESKTOP
        )
        self.assertEqual(len(builtin_keyboard_desktop), 1)
        self.assertEqual(builtin_keyboard_desktop[0].device(), Keyboard.DESKTOP)

        builtin_keyboard_mobile = KeyboardLayoutsMarshall().get_all(
            layout_types="builtin", device=Keyboard.MOBILE
        )
        self.assertEqual(len(builtin_keyboard_mobile), 1)
        self.assertEqual(builtin_keyboard_mobile[0].device(), Keyboard.MOBILE)

    def test_default_keyboards_count(self):
        builtin_keyboards = KeyboardLayoutsMarshall().get(
            device=Keyboard.DESKTOP, layout_id="default"
        )
        self.assertEqual(builtin_keyboards.layout_type(), "builtin")

    def test_builtin_keyboards_fields_match(self):
        """Check the fields in the builtin keyboards match those in the Keyboard model."""
        desktop_keyboard = KeyboardFactory(user=self.user, device_type=Keyboard.DESKTOP)
        builtin_desktop_keyboard = BuiltinKeyboardFactory(device_type=Keyboard.DESKTOP)

        self.assertEqual(
            desktop_keyboard.serialize().keys(),
            builtin_desktop_keyboard.serialize().keys(),
        )

    def test_user_keyboard_count(self):
        user_keyboards = KeyboardLayoutsMarshall(self.user).get_all(layout_types="user")
        self.assertEqual(len(user_keyboards), 2)
        self.assertEqual(user_keyboards[0].layout_type(), "user")
        self.assertEqual(user_keyboards[1].layout_type(), "user")

    def test_all_keyboard_count(self):
        all_keyboards_no_user = KeyboardLayoutsMarshall().get_all()
        self.assertEqual(len(all_keyboards_no_user), 2)

        all_keyboards = KeyboardLayoutsMarshall(self.user).get_all()
        self.assertEqual(len(all_keyboards), 4)
