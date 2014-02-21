from django.core.exceptions import PermissionDenied
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, DestroyModelMixin
from django.contrib import messages
from django.views.generic.edit import UpdateView
from django.core.urlresolvers import reverse

from .models import Keyboard
from .serializers import KeyboardSerializer, KeyboardOnlySerializer, KeyMapSerializer
from .defaults import DEFAULT_KEYBOARD_MAP


class KeyboardView(GenericAPIView, CreateModelMixin, UpdateModelMixin, DestroyModelMixin):
    """Retrieve, update, or delete a keyboard and associated mappings"""
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = KeyboardOnlySerializer

    @staticmethod
    def get_keyboard(user, keyboard_id=None):
        if not keyboard_id:
            try:
                return Keyboard.objects.get(user=user, is_primary=True)
            except Keyboard.DoesNotExist:
                raise
        try:
            keyboard = Keyboard.objects.get(id=keyboard_id)
        except Keyboard.DoesNotExist:
            raise
        if not keyboard.user == user:
            raise PermissionDenied
        return keyboard

    def pre_save(self, obj):
        obj.user = self.request.user
        return obj

    def create(self, request, *args, **kwargs):
        mappings_data = request.DATA.pop('mappings', None)
        keyboard_data = request.DATA

        # Check if we're dealing with one or more mappings
        mapping_serializer = KeyMapSerializer(data=mappings_data, many=True)

        keyboard_serializer = self.get_serializer(data=keyboard_data)

        # Don't create one without the other
        if keyboard_serializer.is_valid():
            if mapping_serializer.is_valid():
                self.pre_save(keyboard_serializer.object)
                keyboard = keyboard_serializer.save()

                new_mappings = mapping_serializer.save()
                keyboard.set_keymaps(new_mappings)
                return Response(status=status.HTTP_201_CREATED)

        errors = dict()
        errors.update(keyboard_serializer.errors)
        errors.update(mapping_serializer.errors)
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            keyboard = self.get_keyboard(request.user, self.kwargs.get('keyboard_id', None))
        except Keyboard.DoesNotExist:
            return Response('Keyboard does not exist', status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied:
            raise PermissionDenied

        # Separate out mappings from keyboard data
        mappings_data = request.DATA.pop('mappings', None)
        keyboard_data = request.DATA

        # Check if we're dealing with one or more mappings
        mapping_serializer = KeyMapSerializer(data=mappings_data, many=True)

        keyboard_serializer = self.get_serializer(keyboard, data=keyboard_data)

        # Don't update one without the other
        # Don't create one without the other
        if keyboard_serializer.is_valid():
            if mapping_serializer.is_valid():
                self.pre_save(keyboard_serializer.object)
                keyboard = keyboard_serializer.save()

                new_mappings = mapping_serializer.save()
                keyboard.set_keymaps(new_mappings)
                return Response(status=status.HTTP_204_NO_CONTENT)

        errors = dict()
        errors.update(keyboard_serializer.errors)
        errors.update(mapping_serializer.errors)
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, keyboard_id=None):
        """Even if keyboard_id is provided, if user is anonymous, they are given the default keyboard
        without an error, this may not be perfect behaviour, but saves excess error handling in the
        front end."""
        if not request.user.id:
            return Response(DEFAULT_KEYBOARD_MAP)

        if keyboard_id:
            try:
                keyboard = self.get_keyboard(request.user, keyboard_id)
            except Keyboard.DoesNotExist:
                return Response('No keyboard found', status=status.HTTP_404_NOT_FOUND)
            except PermissionDenied:
                raise PermissionDenied
            serializer = KeyboardSerializer(keyboard)
            return Response(serializer.data)

        # If the user doesn't have a default keyboard, just give them the DEFAULT_KEYBOARD_MAP
        try:
            keyboard = self.get_keyboard(request.user, keyboard_id)
        except Keyboard.DoesNotExist:
            return Response(DEFAULT_KEYBOARD_MAP)

        # Use the normal keyboard serializer with mappings for GET
        serializer = KeyboardSerializer(keyboard)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        if self.kwargs.get('keyboard_id', None):
            return self.update(request, *args, **kwargs)
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if not self.kwargs.get('keyboard_id', None):
            return Response('No keyboard ID provided', status=status.HTTP_400_BAD_REQUEST)
        try:
            keyboard = self.get_keyboard(request.user, self.kwargs.get('keyboard_id', None))
        except Keyboard.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)
        except PermissionDenied:
            raise PermissionDenied
        keyboard.delete()
        messages.info(request, 'Keyboard deleted successfully')
        return Response(status=status.HTTP_204_NO_CONTENT)