from django.conf import settings
from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Event
from pagoeta.apps.core.functions import get_absolute_uri
from pagoeta.apps.core.serializers import TranslationModelSerializer, ImageField
from pagoeta.apps.places.serializers import PlaceSerializer, PlaceListSerializer


class TypeField(serializers.RelatedField):
    def to_representation(self, value):
        return {
            'code': value.code,
            'name': value.name,
        }


class EventSerializer(TranslationModelSerializer):
    category = TypeField(read_only=True)
    place = PlaceSerializer(read_only=True)
    image = ImageField(read_only=True)
    images = ImageField(many=True, read_only=True)
    startAt = serializers.DateTimeField(source='start_at', read_only=True)
    endAt = serializers.DateTimeField(source='end_at', read_only=True)
    timetable = serializers.SerializerMethodField()
    subEvents = serializers.PrimaryKeyRelatedField(source='subevents', many=True, read_only=True)
    # camelCase some field names
    targetGroup = TypeField(source='target_group', read_only=True)
    targetAge = TypeField(source='target_age', read_only=True)
    isFeatured = serializers.BooleanField(source='is_featured', read_only=True)

    class Meta(object):
        model = Event
        translation_fields = ('name', 'description')
        camel_cased_fields = ('target_group', 'target_age', 'is_featured')
        exclude = camel_cased_fields + ('start_date', 'end_date', 'start_time', 'end_time', 'afternoon_start_time',
                                        'afternoon_end_time', 'is_visible', 'is_superevent', 'parent')

    def get_timetable(self, obj):
        time_format = settings.REST_FRAMEWORK['TIME_FORMAT']
        if obj.start_time:
            hours = [
                (obj.start_time.strftime(time_format), obj.end_time.strftime(time_format)),
            ] if obj.end_time else [(obj.start_time.strftime(time_format),)]

            if obj.afternoon_end_time:
                hours.append((obj.afternoon_start_time.strftime(time_format),
                              obj.afternoon_end_time.strftime(time_format)))
        else:
            hours = ()

        return hours


class EventListSerializer(EventSerializer):
    place = PlaceListSerializer(read_only=True)
    href = serializers.SerializerMethodField()

    class Meta(EventSerializer.Meta):
        exclude = EventSerializer.Meta.exclude + ('images',)

    def get_href(self, obj):
        return get_absolute_uri(reverse('v1:event-detail', (obj.id,)))
