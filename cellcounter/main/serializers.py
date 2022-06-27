from rest_framework import serializers

from .models import CellType


class CellTypeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = CellType
