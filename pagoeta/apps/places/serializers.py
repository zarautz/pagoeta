from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Place
from pagoeta.apps.core.functions import get_absolute_uri
from pagoeta.apps.core.serializers import TranslationModelSerializer


class TypeField(serializers.RelatedField):
    def to_representation(self, value):
        return value.code


class PlaceSerializer(TranslationModelSerializer):
    types = TypeField(many=True, read_only=True)
    events = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    geometry = serializers.SerializerMethodField()

    class Meta(object):
        model = Place
        translation_fields = ('name', 'description')
        exclude = ('latitude', 'longitude', 'price_level')

    def get_geometry(self, obj):
        return {
            'type': 'Point',
            'coordinates': (obj.longitude, obj.latitude),
        }


class PlaceListSerializer(PlaceSerializer):
    href = serializers.SerializerMethodField()

    class Meta(PlaceSerializer.Meta):
        exclude = PlaceSerializer.Meta.exclude + ('url', 'description')

    def get_href(self, obj):
        return get_absolute_uri(reverse('v1:place-detail', [obj.id]))
