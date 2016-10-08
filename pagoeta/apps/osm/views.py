from django.views.decorators.cache import cache_control
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .scrapers import OpenStreeMapScraper


class NodeViewSet(ViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    @cache_control(max_age=7200)
    def list(self, request):
        """
        Get a list of Places.
        ---
        omit_serializer: true
        parameters:
        -   name: types
            paramType: query
            type: string
            description: 'Restricts the results to Places matching the specified OpenStreetMap feature type(s)
                (use comma separated values for multiple types: "amenity:cafe,shop:books").'
        """
        scraper = OpenStreeMapScraper()
        types, types_meta, types_filter = request.GET.get('types', None), 'all', None

        if types:
            types_filter = types.split(',')

        data = scraper.get_nodes(types_filter)

        if types_filter:
            types_meta = {'filter': types_filter, 'count': len(data)}
            if len(types_filter) > 1:
                types_meta['operator'] = 'OR'

        return Response({
            'meta': {
                'lastUpdated': scraper.data['updated_at'],
                'source': scraper.source,
                'totalCount': len(scraper.data['nodes']),
                'types': types_meta,
            },
            'data': data,
        })

    def retrieve(self, request, pk=None):
        """
        Get detailed information about a Place.
        """
        scraper = OpenStreeMapScraper()

        return Response({
            'meta': {
                'lastUpdated': scraper.data['updated_at'],
                'source': scraper.get_source(pk),
            },
            'data': scraper.get_node(pk),
        })


class FeatureViewSet(ViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    @cache_control(max_age=7200)
    def list(self, request):
        """
        Get available Place Types.
        """
        scraper = OpenStreeMapScraper()
        data = scraper.get_features()

        return Response({
            'meta': {
                'lastUpdated': scraper.data['updated_at'],
                'source': scraper.source,
                'totalCount': len(data),
            },
            'data': data,
        })
