from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Event
from .serializers import EventSerializer


class EventViewSet(ReadOnlyModelViewSet):
    queryset = Event.objects.all()

    def list(self, request):
        from_date = int(request.QUERY_PARAMS.get('from', 0))
        to_date = int(request.QUERY_PARAMS.get('to', 0))
        offset = int(request.QUERY_PARAMS.get('offset', 0))
        limit = int(request.QUERY_PARAMS.get('limit', 20))

        queryset = self.get_queryset()[offset:(offset + limit)]
        serializer = EventSerializer(queryset, many=True)

        return Response({
            'meta': {
                'language': request.LANGUAGE_CODE,
                'totalCount': queryset.count()
            },
            'data': serializer.data
        })

    def retrieve(self, request, pk=None):
        serializer = EventSerializer(self.get_object())

        return Response({
            'meta': {
                'language': request.LANGUAGE_CODE
            },
            'data': serializer.data
        })
