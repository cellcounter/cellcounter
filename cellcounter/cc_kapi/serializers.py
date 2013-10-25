from rest_framework import serializers

from .models import KeyMap, Keyboard


class KeyMapSerializer(serializers.ModelSerializer):
    cellid = serializers.PrimaryKeyRelatedField()

    class Meta:
        model = KeyMap
        fields = ('id', 'cellid', 'key')

    def save(self, **kwargs):
        """
        Unintelligent save via get_or_create(). This does not handle logic
        for creating/removing maps from parent models. It merely puts new
        maps into the database.
        """
        # Clear cached _data, which may be invalidated by `save()`
        self._data = None
        if isinstance(self.object, list):
            saved_mappings = [KeyMap.objects.get_or_create(cellid=item.cellid, key=item.key)[0] for item in self.object]
        else:
            saved_mappings = KeyMap.objects.get_or_create(cellid=self.object.cellid, key=self.object.key)[0]
        self.object = saved_mappings
        return self.object


class KeyboardOnlySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    user = serializers.Field(source='user.username')

    class Meta:
        model = Keyboard
        fields = ('id', 'user', 'label', 'is_primary', 'created',
                  'last_modified')


class KeyboardSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    user = serializers.Field(source='user.username')
    mappings = KeyMapSerializer(many=True, read_only=True)

    class Meta:
        model = Keyboard
        fields = ('id', 'user', 'label', 'is_primary', 'created',
                  'last_modified', 'mappings')