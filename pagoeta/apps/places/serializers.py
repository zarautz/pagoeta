from hvad.contrib.restframework import TranslatableModelSerializer
from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Place, Type
from pagoeta.apps.core.functions import get_absolute_uri


class TypeSerializer(TranslatableModelSerializer):
    class Meta(object):
        model = Type
        exclude = ('language_code',)


class PlaceSerializer(TranslatableModelSerializer):
    types = serializers.StringRelatedField(many=True, read_only=True)
    events = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    geometry = serializers.SerializerMethodField()

    class Meta(object):
        model = Place
        exclude = ('latitude', 'longitude', 'price_level', 'language_code')

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
