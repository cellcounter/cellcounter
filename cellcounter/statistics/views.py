from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import BasePermission
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework_xml.renderers import XMLRenderer

from .models import CountInstance
from .serializers import CountInstanceCreateSerializer, CountInstanceModelSerializer

SAFE_METHODS = ["GET", "HEAD", "OPTIONS"]


class OpenPostStaffGet(BasePermission):
    """
    Allows posting by anonymous users, but requires a staff user to GET/HEAD/OPTIONS
    """

    def has_permission(self, request, view):
        if request.method == "POST" or all(
            [
                request.method in SAFE_METHODS,
                request.user.is_authenticated,
                request.user.is_staff,
            ]
        ):
            return True
        return False


class CountInstanceAnonThrottle(AnonRateThrottle):
    rate = "1/minute"


class ListCreateCountInstanceAPI(ListCreateAPIView):
    permission_classes = (OpenPostStaffGet,)
    serializer_class = CountInstanceModelSerializer
    queryset = CountInstance.objects.all()
    throttle_classes = (CountInstanceAnonThrottle,)
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer, XMLRenderer)

    def create(self, request, *args, **kwargs):
        serializer = CountInstanceCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if self.request.user.is_authenticated:
            user = self.request.user
        else:
            user = None
        serializer.save(
            session_id=request.session.session_key,
            ip_address=request.META.get("REMOTE_ADDR"),
            user=user,
        )
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
