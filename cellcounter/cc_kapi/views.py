from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.exceptions import NotFound, ParseError, NotAuthenticated
from rest_framework import status

from .models import Keyboard, DefaultKeyboards
from .serializers import KeyboardSerializer, KeyboardListItemSerializer
from .defaults import BUILTIN_KEYBOARDS
from .defaults import BUILTIN_DESKTOP_KEYBOARD_MAP, BUILTIN_MOBILE_KEYBOARD_MAP
from .marshalls import KeyboardLayoutsMarshall

from rest_framework import viewsets

from django.urls import reverse

import itertools


class KeyboardViewSet(viewsets.ViewSet):
    """
    A ViewSet for manipulating keyboards.
    """

    permission_classes = (IsAuthenticatedOrReadOnly,)

    _device_type = None

    def device_type_display(self):
        return Keyboard.DEVICE_TYPES[self._device_type - 1][1]

    @property
    def device_type(self):
        return self._device_type

    @device_type.setter
    def device_type(self, val):
        self._device_type = val

    def _set_user_default_keyboard(self, user, keyboard):
        """Helper function to set the user's default keyboard."""

        # update or create a default on the user's profile as appropriate
        if not hasattr(user, "defaultkeyboards"):
            defaultkeyboards = DefaultKeyboards.objects.create(user=user)
        else:
            defaultkeyboards = user.defaultkeyboards

        if self.device_type == Keyboard.DESKTOP:
            defaultkeyboards.desktop = keyboard
        elif self.device_type == Keyboard.MOBILE:
            defaultkeyboards.mobile = keyboard

        defaultkeyboards.save()

    def _clear_user_default_keyboard(self, user):
        if not hasattr(user, "defaultkeyboards"):
            return
        defaultkeyboards = user.defaultkeyboards

        if self.device_type == Keyboard.DESKTOP:
            defaultkeyboards.desktop = None
        elif self.device_type == Keyboard.MOBILE:
            defaultkeyboards.mobile = None

        defaultkeyboards.save()

    def list(self, request):
        """List the keyboards available for the current user.

        Can show all keyboards for the top level API, or those restricted to
        either desktop or mobile.
        """

        user = None
        if self.request.user.is_authenticated:
            user = self.request.user

        if self.device_type:
            keyboards = KeyboardLayoutsMarshall(user).get_all(self.device_type)
        else:
            keyboards = KeyboardLayoutsMarshall(user).get_all()

        keyboard_data = []
        for kb in keyboards:
            keyboard_data.append(kb.serialize(many=True))

        return Response(keyboard_data)

    def create(self, request):
        """Create a new keyboard based on request data and set it as the default keyboard."""

        if not self.request.user.is_authenticated:
            raise NotAuthenticated("Method only available to authenticated users")
        user = self.request.user

        serializer = KeyboardSerializer(data=request.data)
        serializer.device_type = self.device_type
        serializer.is_valid(raise_exception=True)
        keyboard = serializer.save(user=user)

        self._set_user_default_keyboard(user, keyboard)

        return Response(request.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        """Retrieve a specific keyboard."""

        user = None

        if self.request.user.is_authenticated:
            user = self.request.user

        keyboard = KeyboardLayoutsMarshall(user).get(pk, self.device_type)

        if not keyboard:
            raise NotFound(
                f"{self.device_type_display()} keyboard with name '{pk}' not found"
            )

        return Response(keyboard.serialize())

    def update(self, request, pk=None):
        """Update a keyboard based on request data."""

        if not self.request.user.is_authenticated:
            raise NotAuthenticated("Method only available to authenticated users")
        user = self.request.user

        try:
            keyboard = Keyboard.objects.get(
                user=user, id=pk, device_type=self.device_type
            )
        except ValueError:
            raise ParseError("Invalid keyboard identifier")
        except Keyboard.DoesNotExist:
            raise NotFound(
                f"{self.device_type_display()} keyboard with id '{pk}' not found"
            )

        serializer = KeyboardSerializer(keyboard, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(request.data)

    def destroy(self, request, pk=None):
        """Destroy a keyboard based on request data."""

        if not self.request.user.is_authenticated:
            raise NotAuthenticated("Method only available to authenticated users")
        user = self.request.user

        try:
            keyboard = Keyboard.objects.get(
                user=user, id=pk, device_type=self.device_type
            )
        except ValueError:
            raise ParseError("Invalid keyboard identifier")
        except Keyboard.DoesNotExist:
            raise NotFound(
                f"{self.device_type_display()} keyboard with id '{pk}' not found"
            )

        # check if the keyboard we are about to delete is the default keyboard
        if hasattr(user, "defaultkeyboards"):
            if (
                self.device_type == Keyboard.DESKTOP
                and hasattr(user.defaultkeyboards, "desktop")
                and user.defaultkeyboards.desktop == keyboard
            ):
                user.defaultkeyboards.desktop = None
            elif (
                self.device_type == Keyboard.MOBILE
                and hasattr(user.defaultkeyboards, "mobile")
                and user.defaultkeyboards.mobile == keyboard
            ):
                user.defaultkeyboards.mobile = None

            user.defaultkeyboards.save()

        keyboard.delete()

        return Response(request.data)

    def set_default(self, request, pk=None):
        """Set the specified keyboard as the user's default."""

        if not self.request.user.is_authenticated:
            raise NotAuthenticated("Method only available to authenticated users")
        user = self.request.user

        if pk == "builtin":
            self._clear_user_default_keyboard(user)
            return Response({"status": "Default cleared"})

        try:
            keyboard = Keyboard.objects.get(
                user=user, id=pk, device_type=self.device_type
            )
        except ValueError:
            raise ParseError("Invalid keyboard identifier")
        except Keyboard.DoesNotExist:
            raise NotFound(
                f"{self.device_type_display()} keyboard with name '{pk}' not found"
            )

        self._set_user_default_keyboard(user, keyboard)
        return Response({"status": "Default set"})
