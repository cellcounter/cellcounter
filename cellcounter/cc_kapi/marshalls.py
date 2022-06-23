from .models import Keyboard
from .serializers import KeyboardSerializer, KeyboardListItemSerializer, BuiltinKeyboardSerializer, BuiltinKeyboardListItemSerializer
from .defaults import BUILTIN_KEYBOARDS

from pydictobject import DictObject

from abc import ABC, abstractmethod

class KeyboardLayoutsMarshall():

    def __init__(self, user=None):
        self.user = user
        self._populate_defaults()

    def _populate_defaults(self):
        self.default_desktop_id = "builtin"
        self.default_mobile_id = "builtin"
        if self.user and hasattr(self.user, 'defaultkeyboards'):
            try:
                self.default_desktop_id = self.user.defaultkeyboards.desktop.id
            except AttributeError:
                pass
            try:
                self.default_mobile_id = self.user.defaultkeyboards.mobile.id or "builtin"
            except AttributeError:
                pass

    def get_all(self, device="all", layout_types="all"):
        if layout_types == "all":
            layout_types = ["builtin", "user"]
        else:
            layout_types = layout_types.split(',')

        keyboards = []

        if "builtin" in layout_types:
            for kb in BUILTIN_KEYBOARDS:
                keyboard = BuiltinKeyboardModel(kb)
                if keyboard.device() == Keyboard.DESKTOP and self.default_desktop_id == "builtin":
                    keyboard.set_default()
                elif keyboard.device() == Keyboard.MOBILE and self.default_mobile_id == "builtin":
                    keyboard.set_default()
                keyboards.append(keyboard)

        if "user" in layout_types:
            user_keyboards = UserKeyboardModel.objects.filter(user=self.user).order_by('id')
            for kb in user_keyboards:
                if kb.device() == Keyboard.DESKTOP and self.default_desktop_id == kb.id:
                    kb.set_default()
                elif kb.device() == Keyboard.MOBILE and self.default_mobile_id == kb.id:
                    kb.set_default()
                keyboards.append(kb)

        # filter by device
        if device != "all":
            keyboards = [kb for kb in keyboards if kb.device() == device]

        return keyboards

    def get(self, layout_id, device):
        """Get the keyboard layout by id for the specified device"""
        if layout_id == "default":
            return self.get_default(device)

        if layout_id == "builtin":
            for kb in BUILTIN_KEYBOARDS:
                keyboard = BuiltinKeyboardModel(kb)
                if keyboard.device() == device:
                    return keyboard
            return None

        

        if self.user:
            try:
                keyboard = UserKeyboardModel.objects.get(user=self.user, id=layout_id, device_type=device)
            except Keyboard.DoesNotExist:
                return None

            return keyboard

        return None

    def get_default(self, device):
        """Get the default keyboard layout for the specified device"""

        if device == Keyboard.DESKTOP:
            return self.get(self.default_desktop_id, Keyboard.DESKTOP)
        elif device == Keyboard.MOBILE:
            return self.get(self.default_mobile_id, Keyboard.MOBILE)

        return None


class KeyboardLayout:

    def serialize(self):
        raise NotImplementedError()

    def set_default(self):
        self._set_default()

    def device(self):
        return self.device_type

    def layout_type(self):
        raise NotImplementedError()


class BuiltinKeyboardModel(DictObject, KeyboardLayout):

    def __init__(self, *args, **kwargs):
        self.is_default = False
        super().__init__(*args, **kwargs)

    def _set_default(self):
        self.is_default = True

    def serializer(self):
        return "json"

    def serialize(self, many=False):
        if many:
            return BuiltinKeyboardListItemSerializer(self).data
        return BuiltinKeyboardSerializer(self).data
        if many:
            self.pop("mappings")
        else:
            self.pop("is_default")
        return self

    def layout_type(self):
        return "builtin"

    def get_device_type_display(self):
        try:
            return [x for i, x in Keyboard.DEVICE_TYPES if i == self.device_type][0]
        except IndexError:
            return None


class UserKeyboardModel(Keyboard, KeyboardLayout):
    def serialize(self, many=False):
        if many:
            return KeyboardListItemSerializer(self).data
        return KeyboardSerializer(self).data

    def layout_type(self):
        return "user"

    class Meta:
        proxy = True


