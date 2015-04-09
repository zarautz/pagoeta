from django.conf import settings
from hvad.contrib.restframework import TranslatableModelSerializer
from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Place, Type


class TypeSerializer(TranslatableModelSerializer):
    class Meta(object):
        model = Type
        exclude = ('language_code',)


class PlaceSerializer(TranslatableModelSerializer):
    types = serializers.StringRelatedField(many=True, read_only=True)
    events = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    geometry = serializers.SerializerMethodField()
    href = serializers.SerializerMethodField()

    class Meta(object):
        model = Place
        exclude = ('latitude', 'longitude', 'price_level', 'language_code')

    def get_geometry(self, obj):
        return {
            'type': 'Point',
            'coordinates': (obj.longitude, obj.latitude)
        }

    def get_href(self, obj):
        return '%s%s' % (settings.BASE_URL, reverse('v1:place-detail', [obj.id]))


class PlaceListSerializer(PlaceSerializer):
    class Meta(PlaceSerializer.Meta):
        exclude = PlaceSerializer.Meta.exclude + ('url', 'description')
