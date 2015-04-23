from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Event
from pagoeta.apps.core.functions import get_absolute_uri, get_image_sources
from pagoeta.apps.core.serializers import TranslationModelSerializer
from pagoeta.apps.places.serializers import PlaceListSerializer


class ImageField(serializers.RelatedField):
    def to_representation(self, value):
        return {
            'source': get_image_sources('event', value.hash),
            'isFeatured': value.is_featured,
        }


class TypeField(serializers.RelatedField):
    def to_representation(self, value):
        return {
            'code': value.code,
            'name': value.name,
        }


class EventSerializer(TranslationModelSerializer):
    category = TypeField(read_only=True)
    place = PlaceListSerializer(read_only=True)
    image = ImageField(read_only=True)
    images = ImageField(many=True, read_only=True)
    # camelCase some field names
    targetGroup = TypeField(source='target_group', read_only=True)
    targetAge = TypeField(source='target_age', read_only=True)
    startAt = serializers.DateTimeField(source='start_at', read_only=True)
    endAt = serializers.DateTimeField(source='end_at', read_only=True)
    isFeatured = serializers.BooleanField(source='is_featured', read_only=True)

    class Meta(object):
        model = Event
        translation_fields = ('name', 'description')
        camel_cased_fields = ('target_group', 'target_age', 'start_at', 'end_at', 'is_featured')
        exclude = camel_cased_fields + ('is_visible',)


class EventListSerializer(EventSerializer):
    href = serializers.SerializerMethodField()

    class Meta(EventSerializer.Meta):
        exclude = EventSerializer.Meta.exclude + ('images',)

    def get_href(self, obj):
        return get_absolute_uri(reverse('v1:event-detail', (obj.id,)))
