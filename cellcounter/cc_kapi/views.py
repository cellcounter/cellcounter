from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.exceptions import NotFound, ParseError, NotAuthenticated
from rest_framework import status

from .models import Keyboard, DefaultKeyboards
from .serializers import KeyboardSerializer, KeyboardListItemSerializer

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
        return Keyboard.DEVICE_TYPES[self._device_type-1][1]

    @property
    def device_type(self):
        return self._device_type

    @device_type.setter
    def device_type(self, val):
        self._device_type = val

    def _set_user_default_keyboard(self, user, keyboard):
        """Helper function to set the user's default keyboard.
        """

        # update or create a default on the user's profile as appropriate
        if not hasattr(user, 'defaultkeyboards'):
            defaultkeyboards = DefaultKeyboards.objects.create(user=user)
        else:
            defaultkeyboards = user.defaultkeyboards

        if self.device_type == Keyboard.DESKTOP:
            defaultkeyboards.desktop = keyboard
        elif self.device_type == Keyboard.MOBILE:
            defaultkeyboards.mobile = keyboard

        defaultkeyboards.save()

    def _clear_user_default_keyboard(self, user):
        if not hasattr(user, 'defaultkeyboards'):
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

        # get the builtin keyboard maps
        builtin_keyboards = Keyboard.objects.filter(user=None)

        # get any user specific keyboard maps
        user_keyboards = []
        user = None
        if self.request.user.is_authenticated:
            user = self.request.user
            user_keyboards = Keyboard.objects.filter(user=user).order_by('id')

        # set the default flags appropriately
        default_desktop, default_mobile = None, None
        if hasattr(user, 'defaultkeyboards'):
            default_desktop = user.defaultkeyboards.desktop
            default_mobile = user.defaultkeyboards.mobile
        if not default_desktop:
            [builtin_keyboard._set_default() for builtin_keyboard in builtin_keyboards if builtin_keyboard.device_type == Keyboard.DESKTOP]
        else:
            [user_keyboard._set_default() for user_keyboard in user_keyboards if user_keyboard.id == default_desktop.id]
        if not default_mobile:
            [builtin_keyboard._set_default() for builtin_keyboard in builtin_keyboards if builtin_keyboard.device_type == Keyboard.MOBILE]
        else:
            [user_keyboard._set_default() for user_keyboard in user_keyboards if user_keyboard.id == default_mobile.id]

        # combine builtin and user keyboards into the final list
        keyboards = itertools.chain(builtin_keyboards, user_keyboards)

        # filter by device type
        if self.device_type:
            keyboards = [kb for kb in keyboards if kb.device_type == self.device_type]

        # serialise all requested keyboards
        keyboard_list = KeyboardListItemSerializer(keyboards, many=True)

        return Response(keyboard_list.data)


    def create(self, request):
        """Create a new keyboard based on request data and set it as the default keyboard.
        """

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
        """Retrieve a specific keyboard.
        """

        keyboard = None

        if pk == 'default':
            pk = 'builtin'
            if self.request.user.is_authenticated:
                if hasattr(self.request.user, 'defaultkeyboards'):
                    if self.device_type == Keyboard.DESKTOP and \
                            hasattr(self.request.user.defaultkeyboards.desktop, 'id'):
                        pk = self.request.user.defaultkeyboards.desktop.id
                    elif self.device_type == Keyboard.MOBILE and \
                            hasattr(self.request.user.defaultkeyboards.mobile, 'id'):
                        pk = self.request.user.defaultkeyboards.mobile.id

        if pk == 'builtin':
            try:
                keyboard = Keyboard.objects.get(user=None, device_type=self.device_type)
            except Keyboard.DoesNotExist:
                raise NotFound(f"{self.device_type_display()} keyboard with name '{pk}' not found")

        elif self.request.user.is_authenticated:
            try:
                keyboard = Keyboard.objects.get(user=self.request.user, id=pk, device_type=self.device_type)
            except Keyboard.DoesNotExist:
                raise NotFound(f"{self.device_type_display()} keyboard with id '{pk}' not found")

        if not keyboard:
            raise NotAuthenticated("Method only available to authenticated users")

        serializer = KeyboardSerializer(keyboard)
        return Response(serializer.data)


    def update(self, request, pk=None):
        """Update a keyboard based on request data.
        """

        if not self.request.user.is_authenticated:
            raise NotAuthenticated("Method only available to authenticated users")
        user = self.request.user

        try:
            keyboard = Keyboard.objects.get(user=user, id=pk, device_type=self.device_type)
        except ValueError:
            raise ParseError('Invalid keyboard identifier')
        except Keyboard.DoesNotExist:
            raise NotFound(f"{self.device_type_display()} keyboard with id '{pk}' not found")

        serializer = KeyboardSerializer(keyboard, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(request.data)


    def destroy(self, request, pk=None):
        """Destroy a keyboard based on request data.
        """

        if not self.request.user.is_authenticated:
            raise NotAuthenticated("Method only available to authenticated users")
        user = self.request.user

        try:
            keyboard = Keyboard.objects.get(user=user, id=pk, device_type=self.device_type)
        except ValueError:
            raise ParseError('Invalid keyboard identifier')
        except Keyboard.DoesNotExist:
            raise NotFound(f"{self.device_type_display()} keyboard with id '{pk}' not found")

        # check if the keyboard we are about to delete is the default keyboard
        if hasattr(user, 'defaultkeyboards'):
            if self.device_type == Keyboard.DESKTOP and \
               hasattr(user.defaultkeyboards, 'desktop') and \
               user.defaultkeyboards.desktop == keyboard:
                user.defaultkeyboards.desktop = None
            elif self.device_type == Keyboard.MOBILE and \
               hasattr(user.defaultkeyboards, 'mobile') and \
               user.defaultkeyboards.mobile == keyboard:
                user.defaultkeyboards.mobile = None

            user.defaultkeyboards.save()

        keyboard.delete()

        return Response(request.data)


    def set_default(self, request, pk=None):
        """Set the specified keyboard as the user's default.
        """

        if not self.request.user.is_authenticated:
            raise NotAuthenticated("Method only available to authenticated users")
        user = self.request.user

        if pk == 'builtin':
            self._clear_user_default_keyboard(user)
            return Response({'status': 'Default cleared'})

        try:
            keyboard = Keyboard.objects.get(user=user, id=pk, device_type=self.device_type)
        except ValueError:
            raise ParseError('Invalid keyboard identifier')
        except Keyboard.DoesNotExist:
            raise NotFound(f"{self.device_type_display()} keyboard with name '{pk}' not found")

        self._set_user_default_keyboard(user, keyboard)
        return Response({'status': 'Default set'})


