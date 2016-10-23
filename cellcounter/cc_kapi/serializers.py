from rest_framework import serializers

from .models import KeyMap, Keyboard


from django.core.urlresolvers import reverse


class KeyMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyMap
        fields = ('cellid', 'key')

#href = HrefField(view_name='keyboards-desktop-detail')
#href = serializers.HyperlinkedIdentityField(view_name='keyboards-desktop-detail')

class KeyboardListItemSerializer(serializers.ModelSerializer):
    """Serialises a list of keyboards with hrefs.
    """

    class Meta:
        model = Keyboard
        fields = ('id', 'user', 'label', 'created',
                  'last_modified','is_default', 'device_type','href')
        read_only_fields = ('href',)

    id = serializers.IntegerField(required=False)
    user = serializers.CharField(source='user.username', allow_null=True)
    device_type = serializers.SerializerMethodField()

    is_default = serializers.BooleanField()

    # XXX: This is a hack but I can't get HyperlinkedIdentityField to work, which
    #      seems like it should be the right answer
    href = serializers.SerializerMethodField('get_api_url')
    def get_api_url(self, obj):
        if obj.user:
            return reverse('keyboards-%s-detail' % obj.get_device_type_display(), kwargs={'pk': obj.id})
        else:
            return reverse('keyboards-%s-detail' % obj.get_device_type_display(), kwargs={'pk': 'builtin'})

    def get_device_type(self,obj):
        return obj.get_device_type_display()


class KeyboardSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    user = serializers.CharField(source='user.username', allow_null=True)
    device_type = serializers.ChoiceField(choices=Keyboard.DEVICE_TYPES)
    mappings = KeyMapSerializer(many=True)

    class Meta:
        model = Keyboard
        fields = ('id', 'user', 'label', 'created',
                  'last_modified', 'device_type', 'mappings')

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
        instance.save()

        mapping_objects = [KeyMap.objects.get_or_create(cellid=mapping['cellid'], key=mapping['key'])[0] for
                           mapping in mappings_data]
        instance.set_keymaps(mapping_objects)
        return instance
