from datetime import datetime, timedelta
from django.utils import timezone
from django.views.decorators.cache import cache_control
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Event
from .serializers import EventSerializer, EventListSerializer


class EventViewSet(ReadOnlyModelViewSet):
    queryset = Event.objects.visible() \
                            .prefetch_related('category', 'target_group', 'target_age', 'images',
                                              'place__images', 'place__types')
    serializer_class = EventSerializer
    DEFAULT_DAYS_DIFFERENCE = 30
    MAX_DAYS_DIFFERENCE = 180

    @cache_control(max_age=3600, s_maxage=3600)
    def list(self, request):
        """
        Get a list of Events between two dates, ordered by date (ASC).
        ---
        omit_serializer: true
        parameters:
        -   name: language
            paramType: query
            type: string
            description: ISO 639-1 language code.
            enum: [eu, es, en, fr]
            defaultValue: eu
        -   name: from
            paramType: query
            type: date
            description: ISO 8601 YYYY-MM-DD date format.
        -   name: to
            paramType: query
            type: date
            description: ISO 8601 YYYY-MM-DD date format. Maximum difference can be 180 days.
        """
        try:
            date_format = '%Y-%m-%d'
            today_str = datetime.strftime(datetime.now(), date_format)
            from_date = timezone.make_aware(datetime.strptime(request.GET.get('from', today_str), date_format),
                                            timezone.get_current_timezone())
            default_to_str = datetime.strftime(from_date + timedelta(days=self.DEFAULT_DAYS_DIFFERENCE), date_format)
            to_date = timezone.make_aware(datetime.strptime(request.GET.get('to', default_to_str), date_format),
                                          timezone.get_current_timezone())
        except ValueError:
            raise ParseError('Date format should be ISO 8601 YYYY-MM-DD.')

        if (to_date - from_date).days > self.MAX_DAYS_DIFFERENCE:
            raise ParseError('Difference between dates cannot be more than %d days.' % self.MAX_DAYS_DIFFERENCE)

        queryset = self.queryset.filter(start_date__gte=from_date, end_date__lte=to_date)
        serializer = EventListSerializer(queryset, many=True)
        data = serializer.data

        return Response({
            'meta': {
                'language': request.LANGUAGE_CODE,
                'from': from_date,
                'to': to_date,
                'totalCount': len(data),
            },
            'data': data,
        })

    @cache_control(max_age=7200, s_maxage=7200)
    def retrieve(self, request, pk=None):
        """
        Get full information of an Event, including the related Place model.
        ---
        omit_serializer: true
        parameters:
        -   name: language
            paramType: query
            type: string
            description: ISO 639-1 language code.
            enum: [eu, es, en, fr]
            defaultValue: eu
        """
        serializer = EventSerializer(self.get_object())

        return Response({
            'meta': {
                'language': request.LANGUAGE_CODE,
            },
            'data': serializer.data,
        })
