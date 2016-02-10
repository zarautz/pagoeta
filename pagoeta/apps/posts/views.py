from django.views.decorators.cache import cache_control
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .scrapers import ZuZarautzPostScraper


class ZuZarautzPostViewSet(ViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    @cache_control(max_age=7200)
    def list(self, request):
        """
        Get the latest Zu Zarautz news (language="eu").
        """
        scraper = ZuZarautzPostScraper()
        data = scraper.get_data()

        return Response({
            'meta': {
                'language': 'eu',
                'lastUpdated': scraper.updated,
                'source': scraper.get_source(),
                'totalCount': len(data),
            },
            'data': data,
        })
