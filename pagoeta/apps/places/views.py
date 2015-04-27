from django.views.decorators.cache import cache_control
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, ReadOnlyModelViewSet

from .models import Place, Type
from .serializers import PlaceSerializer, PlaceListSerializer


class PlaceViewSet(ReadOnlyModelViewSet):
    queryset = Place.objects.visible().prefetch_related('types', 'images')
    serializer_class = PlaceSerializer
    DEFAULT_LIMIT = 20
    MAX_LIMIT = 50

    @cache_control(max_age=7200, s_maxage=7200)
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
            offset = int(request.GET.get('offset', 0))
            limit = int(request.GET.get('limit', self.DEFAULT_LIMIT))
            types, types_meta = request.GET.get('types', None), None
        except ValueError:
            raise ParseError('Offset and limit should be numeric.')

        if offset < 0:
            raise ParseError('Offset should not be lower than 0.')

        if limit > self.MAX_LIMIT:
            raise ParseError('Limit cannot be higher than %d.' % self.MAX_LIMIT)

        if types:
            if ',' in types and ' ' in types:
                raise ParseError('Only one operator in allowed for `types`: OR (,) or AND (+).')
            elif ' ' in types:
                types_meta = {
                    'filter': types.split(' '),
                    'operator': 'AND',
                }
                for type_code in types_meta['filter']:
                    self.queryset = self.queryset.filter(types__code=type_code)
            else:
                types_filter = types.split(',')
                types_meta = {
                    'filter': types_filter,
                    'operator': 'OR' if len(types_filter) > 1 else None,
                }
                self.queryset = self.queryset.filter(types__code__in=types_filter)

        queryset = self.queryset[offset:(offset + limit)]
        serializer = PlaceListSerializer(queryset, many=True)

        return Response({
            'meta': {
                'language': request.LANGUAGE_CODE,
                'offset': offset,
                'limit': limit,
                'types': types_meta,
                'totalCount': Place.objects.visible().count(),
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

    @cache_control(max_age=86400, s_maxage=86400)
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

        for item in self.queryset:
            data[item.code] = {
                'name': item.name,
            }

        return Response({
            'meta': {
                'language': request.LANGUAGE_CODE,
                'totalCount': len(data),
            },
            'data': data,
        })
