from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Place, Type
from .serializers import PlaceSerializer, PlaceListSerializer


class PlaceViewSet(ReadOnlyModelViewSet):
    queryset = Place.objects.language().all()

    def get_queryset(self):
        return Place.objects.prefetch_related('types', 'events').all()

    def list(self, request):
        offset = int(request.QUERY_PARAMS.get('offset', 0))
        offset = offset if offset > 0 else 0
        limit = int(request.QUERY_PARAMS.get('limit', 20))
        limit = limit if limit <= 50 else 50
        types = request.QUERY_PARAMS.get('types', None)

        if types:
            pass

        queryset = self.get_queryset()[offset:(offset + limit)]
        serializer = PlaceListSerializer(queryset, many=True)

        return Response({
            'meta': {
                'language': request.LANGUAGE_CODE,
                'offset': offset,
                'limit': limit,
                'types': types,
                'totalCount': Place.objects.count()
            },
            'data': serializer.data
        })

    def retrieve(self, request, pk=None):
        serializer = PlaceSerializer(self.get_object())

        return Response({
            'meta': {
                'language': request.LANGUAGE_CODE
            },
            'data': serializer.data
        })


class TypeViewSet(ReadOnlyModelViewSet):
    queryset = Type.objects.all()

    def list(self, request):
        data = {}

        for item in Type.objects.all():
            data[item.code] = {
                'name': item.name
            }

        return Response({
            'meta': {
                'language': request.LANGUAGE_CODE,
                'totalCount': Type.objects.count()
            },
            'data': data
        })
