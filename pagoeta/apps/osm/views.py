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
            types_meta = {'filter': types_filter}
            if len(types_filter) > 1:
                types_meta['operator'] = 'OR'

        data = scraper.get_nodes(types_filter)

        return Response({
            'meta': {
                'lastUpdated': scraper.get_updated_at(),
                'totalCount': len(data),
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
                'lastUpdated': scraper.get_updated_at(),
                'url': 'https://www.openstreetmap.org/node/%s' % pk
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
                'lastUpdated': scraper.get_updated_at(),
                'totalCount': len(data),
            },
            'data': data,
        })
