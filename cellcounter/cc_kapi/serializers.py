from rest_framework import serializers

from .models import KeyMap, Keyboard
from django.contrib.auth.models import User

from django.urls import reverse


class KeyMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyMap
        fields = ("cellid", "key")


class KeyboardListItemSerializer(serializers.ModelSerializer):
    """Serialises a list of keyboards with hrefs."""

    class Meta:
        model = Keyboard
        fields = (
            "id",
            "user",
            "label",
            "created",
            "last_modified",
            "is_default",
            "device_type",
            "href",
        )
        read_only_fields = ("href",)

    id = serializers.IntegerField(required=False)
    user = serializers.CharField(source="user.username")  # , allow_null=True)
    device_type = serializers.SerializerMethodField()

    is_default = serializers.BooleanField()

    # XXX: This is a hack but I can't get HyperlinkedIdentityField to work, which
    #      seems like it should be the right answer
    href = serializers.SerializerMethodField("get_api_url")

    def get_api_url(self, obj):
        return reverse(
            "keyboards-%s-detail" % obj.get_device_type_display(), kwargs={"pk": obj.id}
        )

    def get_device_type(self, obj):
        return obj.get_device_type_display()


class ChoiceField(serializers.ChoiceField):
    def to_representation(self, obj):
        if obj == "" and self.allow_blank:
            return obj
        return self._choices[obj]

    def to_internal_value(self, data):
        # To support inserts with the value
        if data == "" and self.allow_blank:
            return ""

        for key, val in self._choices.items():
            if val == data:
                return key
        self.fail("invalid_choice", input=data)


class KeyboardSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    user = serializers.CharField(
        source="user.username", allow_null=True, required=False
    )
    device_type = ChoiceField(choices=Keyboard.DEVICE_TYPES)
    mappings = KeyMapSerializer(many=True)

    class Meta:
        model = Keyboard
        fields = (
            "id",
            "user",
            "label",
            "created",
            "last_modified",
            "device_type",
            "mappings",
        )

    def create_from_self(self):
        return self.create(self.validated_data)

    def create(self, validated_data):
        mappings_data = validated_data.pop("mappings")
        keyboard = Keyboard.objects.create(**validated_data)
        mapping_objects = [
            KeyMap.objects.get_or_create(cellid=mapping["cellid"], key=mapping["key"])[
                0
            ]
            for mapping in mappings_data
        ]
        keyboard.set_keymaps(mapping_objects)
        return keyboard

    def update(self, instance, validated_data):
        mappings_data = validated_data.pop("mappings")
        instance.label = validated_data.get("label", instance.label)
        instance.save()

        mapping_objects = [
            KeyMap.objects.get_or_create(cellid=mapping["cellid"], key=mapping["key"])[
                0
            ]
            for mapping in mappings_data
        ]
        instance.set_keymaps(mapping_objects)
        return instance


class MappingList(serializers.Serializer):
    cellid = serializers.IntegerField()
    key = serializers.CharField()


class BuiltinKeyboardSerializer(serializers.Serializer):
    id = serializers.CharField(required=False)
    user = serializers.CharField(required=False)
    device_type = serializers.SerializerMethodField()
    label = serializers.CharField()
    created = serializers.DateTimeField()
    last_modified = serializers.DateTimeField()

    mappings = MappingList(many=True)

    def get_device_type(self, obj):
        return obj.get_device_type_display()


class BuiltinKeyboardListItemSerializer(serializers.Serializer):
    id = serializers.CharField(required=False)
    user = serializers.CharField(required=False)
    device_type = serializers.SerializerMethodField()
    label = serializers.CharField()
    created = serializers.DateTimeField()
    last_modified = serializers.DateTimeField()

    is_default = serializers.BooleanField()

    href = serializers.SerializerMethodField("get_api_url")

    def get_api_url(self, obj):
        return reverse(
            "keyboards-%s-detail" % obj.get_device_type_display(),
            kwargs={"pk": "builtin"},
        )

    def get_device_type(self, obj):
        return obj.get_device_type_display()
