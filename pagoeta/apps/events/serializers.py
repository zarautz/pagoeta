from django.conf import settings
from hvad.contrib.restframework import TranslatableModelSerializer
from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Category, TargetGroup, TargetAge, Event
from pagoeta.apps.places.serializers import PlaceListSerializer


class TypeField(serializers.RelatedField):
    def to_representation(self, value):
        return {
            'code': value.code,
            'name': value.name
        }


class EventSerializer(TranslatableModelSerializer):
    category = TypeField(read_only=True)
    targetGroup = target_group = TypeField(read_only=True)
    targetAge = target_age = TypeField(read_only=True)
    place = PlaceListSerializer(read_only=True)
    # camelCase some field names
    startAt = serializers.DateTimeField(source='start_at', read_only=True)
    endAt = serializers.DateTimeField(source='end_at', read_only=True)
    isFeatured = serializers.BooleanField(source='is_featured', read_only=True)
    isVisible = serializers.BooleanField(source='is_visible', read_only=True)
    href = serializers.SerializerMethodField()

    class Meta(object):
        model = Event
        exclude = ('start_at', 'end_at', 'is_featured', 'is_visible', 'language_code')

    def get_href(self, obj):
        return '%s%s' % (settings.BASE_URL, reverse('v1:event-detail', [obj.id]))
