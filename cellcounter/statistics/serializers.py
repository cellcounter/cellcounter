from rest_framework.serializers import ModelSerializer
from .models import CountInstance


class CountInstanceCreateSerializer(ModelSerializer):
    class Meta:
        fields = "__all__"
        model = CountInstance
        fields = ("count_total",)


class CountInstanceModelSerializer(ModelSerializer):
    class Meta:
        fields = "__all__"
        model = CountInstance
