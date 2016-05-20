from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Keyboard
from .serializers import KeyboardSerializer
from .defaults import DEFAULT_KEYBOARD_MAP


class DefaultKeyboardView(generics.RetrieveAPIView):
    """This returns either the DEFAULT_KEYBOARD_MAP, or the user's
        primary keyboard"""
    serializer_class = KeyboardSerializer

    def get_object(self):
        return Keyboard.objects.get(user=self.request.user, default=True)

    def retrieve(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return Response(DEFAULT_KEYBOARD_MAP)

        try:
            instance = self.get_object()
        except Keyboard.DoesNotExist:
            return Response(DEFAULT_KEYBOARD_MAP)

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class KeyboardsListCreateView(generics.ListCreateAPIView):
    """Lists all a user's keyboards, allows creation of new keyboards,
       denies access to AnonymousUsers"""
    permission_classes = (IsAuthenticated,)
    serializer_class = KeyboardSerializer

    def get_queryset(self):
        return Keyboard.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class KeyboardGetUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """Gets, Updates and Destroys keyboards"""
    permission_classes = (IsAuthenticated,)
    serializer_class = KeyboardSerializer
    lookup_url_kwarg = "keyboard_id"

    def get_queryset(self):
        return Keyboard.objects.filter(user=self.request.user)
