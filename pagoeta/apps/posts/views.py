from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, ReadOnlyModelViewSet

from .scrapers import ZuZarautzPostScraper


class ZuZarautzPostViewSet(ViewSet):
    """
    Get the latest Zu Zarautz news.
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def list(self, request):
        scraper = ZuZarautzPostScraper()
        data = scraper.get_data()

        response = Response({
            "meta": {
                "language": "eu",
                "lastUpdated": scraper.updated,
                "source": scraper.get_source(),
                "totalCount": len(data)
            },
            'data': data
        })
        response['Cache-Control'] = 'public, max-age=%s' % scraper.cache_timeout

        return response
