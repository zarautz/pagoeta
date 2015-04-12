from datetime import datetime, timedelta
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Event
from .serializers import EventSerializer


class EventViewSet(ReadOnlyModelViewSet):
    queryset = Event.objects.order_by('start_at').all()
    serializer_class = EventSerializer

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
            from_date = datetime.strptime(request.QUERY_PARAMS.get('from', today_str), date_format)
            default_to_str = datetime.strftime(from_date + timedelta(days=30), date_format)
            to_date = datetime.strptime(request.QUERY_PARAMS.get('to', default_to_str), date_format)
        except ValueError:
            raise ParseError('Date format should be ISO 8601 YYYY-MM-DD.')

        if (to_date - from_date).days > 180:
            raise ParseError('Difference between dates cannot be more than 180 days.')

        queryset = self.queryset.filter(start_at__gte=from_date, end_at__lte=to_date)
        serializer = EventSerializer(queryset, many=True)

        return Response({
            'meta': {
                'language': request.LANGUAGE_CODE,
                'from': from_date,
                'to': to_date,
                'totalCount': queryset.count(),
            },
            'data': serializer.data,
        })

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
