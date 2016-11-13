from rest_framework import serializers

from .models import CellType


class CellTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CellType
        fields = '__all__'
