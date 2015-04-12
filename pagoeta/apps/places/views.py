from django.db.models import Q
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, ReadOnlyModelViewSet

from .models import Place, Type
from .serializers import PlaceSerializer, PlaceListSerializer


class PlaceViewSet(ReadOnlyModelViewSet):
    queryset = Place.objects.prefetch_related('types').all()
    serializer_class = PlaceSerializer

    def list(self, request):
        """
        Get a list of Places.
        ---
        omit_serializer: true
        parameters:
        -   name: language
            paramType: query
            type: string
            description: ISO 639-1 language code.
            enum: [eu, es, en, fr]
            defaultValue: eu
        -   name: offset
            paramType: query
            type: integer
            description: Offset the list of returned Places by this amount.
            defaultValue: 0
            minimum: 0
        -   name: limit
            paramType: query
            type: integer
            description: Number of Places to return, up to a maximum of 50.
            defaultValue: 20
            minimum: 1
            maximum: 50
        -   name: types
            paramType: query
            type: string
            description: 'Restricts the results to Places matching at least ONE of the specified
                Type `code`s (when using comma separated values: "typeCode1,typeCode2") or ALL the
                specified Type `code`s (when using "+" separated values: "typeCode1+typeCode2").'
        """
        try:
            offset = int(request.QUERY_PARAMS.get('offset', 0))
            limit = int(request.QUERY_PARAMS.get('limit', 20))
            types, types_meta = request.QUERY_PARAMS.get('types', None), None
        except ValueError:
            raise ParseError('Offset and limit should be numeric.')

        if offset < 0:
            raise ParseError('Offset should not be lower than 0.')

        if limit > 50:
            raise ParseError('Limit cannot be higher than 50.')

        if types:
            if ',' in types:
                types_meta = {
                    'filter': types.split(','),
                    'operator': 'OR',
                }
                self.queryset = self.queryset.filter(types__code__in=types_meta['filter'])
            if ' ' in types:
                if types_meta:
                    raise ParseError('Only one operator in allowed for `types`: OR (,) or AND (+).')
                types_meta = {
                    'filter': types.split(' '),
                    'operator': 'AND',
                }
                for type_code in types_meta['filter']:
                    self.queryset = self.queryset.filter(types__code=type_code)

        queryset = self.queryset[offset:(offset + limit)]
        serializer = PlaceListSerializer(queryset, many=True)

        return Response({
            'meta': {
                'language': request.LANGUAGE_CODE,
                'offset': offset,
                'limit': limit,
                'types': types_meta,
                'totalCount': Place.objects.count(),
            },
            'data': serializer.data,
        })

    def retrieve(self, request, pk=None):
        """
        Get detailed information about a Place.
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
        serializer = PlaceSerializer(self.get_object())

        return Response({
            'meta': {
                'language': request.LANGUAGE_CODE,
            },
            'data': serializer.data,
        })


class TypeViewSet(ViewSet):
    queryset = Type.objects.all()

    def list(self, request):
        """
        Get available Place Types.
        ---
        parameters:
        -   name: language
            paramType: query
            type: string
            description: ISO 639-1 language code.
            enum: [eu, es, en, fr]
            defaultValue: eu
        """
        data = {}

        for item in Type.objects.all():
            data[item.code] = {
                'name': item.name,
            }

        return Response({
            'meta': {
                'language': request.LANGUAGE_CODE,
                'totalCount': Type.objects.count(),
            },
            'data': data,
        })
