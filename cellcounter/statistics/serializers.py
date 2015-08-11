from rest_framework.serializers import ModelSerializer
from .models import CountInstance


class CountInstanceSerializer(ModelSerializer):
    class Meta:
        model = CountInstance
