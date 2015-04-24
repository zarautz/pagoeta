from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Place
from pagoeta.apps.core.functions import get_absolute_uri
from pagoeta.apps.core.serializers import TranslationModelSerializer, ImageField


class TypeField(serializers.RelatedField):
    def to_representation(self, value):
        return value.code


class PlaceSerializer(TranslationModelSerializer):
    types = TypeField(many=True, read_only=True)
    events = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    geometry = serializers.SerializerMethodField()
    image = ImageField(read_only=True)
    images = ImageField(many=True, read_only=True)

    class Meta(object):
        model = Place
        translation_fields = ('name', 'description')
        exclude = ('latitude', 'longitude', 'price_level', 'is_visible')

    def get_geometry(self, obj):
        return {
            'type': 'Point',
            'coordinates': (obj.longitude, obj.latitude),
        }


class PlaceListSerializer(PlaceSerializer):
    href = serializers.SerializerMethodField()

    class Meta(PlaceSerializer.Meta):
        exclude = PlaceSerializer.Meta.exclude + ('url', 'description', 'events', 'images')

    def get_href(self, obj):
        return get_absolute_uri(reverse('v1:place-detail', (obj.id,)))
