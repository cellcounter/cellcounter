from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import BasePermission
from rest_framework.throttling import AnonRateThrottle
from .serializers import CountInstanceSerializer
from .models import CountInstance

SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']


class OpenPostStaffGet(BasePermission):
    """
    Allows posting by anonymous users, but requires a staff user to GET/HEAD/OPTIONS
    """
    def has_permission(self, request, view):
        if (request.method == 'POST' or
            request.method in SAFE_METHODS and
            request.user.is_authenticated() and
            request.user.is_staff):
                return True
        return False


class CountInstanceAnonThrottle(AnonRateThrottle):
    rate = '1/minute'


class ListCreateCountInstanceAPI(ListCreateAPIView):
    permission_classes = (OpenPostStaffGet,)
    serializer_class = CountInstanceSerializer
    queryset = CountInstance.objects.all()
    throttle_classes = (CountInstanceAnonThrottle,)
