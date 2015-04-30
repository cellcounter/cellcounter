from rest_framework import serializers

from .models import KeyMap, Keyboard


class KeyMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyMap
        fields = ('cellid', 'key')


class KeyboardOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyboard
        fields = ('id', 'user', 'label', 'is_primary', 'created',
                  'last_modified')


class KeyboardSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    user = serializers.CharField(source='user.username', allow_null=True)
    mappings = KeyMapSerializer(many=True)

    class Meta:
        model = Keyboard
        fields = ('id', 'user', 'label', 'is_primary', 'created',
                  'last_modified', 'mappings')

    def create(self, validated_data):
        mappings_data = validated_data.pop('mappings')
        keyboard = Keyboard.objects.create(**validated_data)
        mapping_objects = [KeyMap.objects.get_or_create(cellid=mapping['cellid'], key=mapping['key'])[0] for
                           mapping in mappings_data]
        keyboard.set_keymaps(mapping_objects)
        return keyboard

    def update(self, instance, validated_data):
        mappings_data = validated_data.pop('mappings')
        instance.label = validated_data.get('label', instance.label)
        instance.is_primary = validated_data.get('is_primary', instance.is_primary)
        instance.save()

        mapping_objects = [KeyMap.objects.get_or_create(cellid=mapping['cellid'], key=mapping['key'])[0] for
                           mapping in mappings_data]
        instance.set_keymaps(mapping_objects)
        return instance