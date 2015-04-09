from django.views.decorators.cache import cache_control
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, ReadOnlyModelViewSet

from .scrapers import ZuZarautzPostScraper


class ZuZarautzPostViewSet(ViewSet):
    """
    Get the latest Zu Zarautz news.
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)

    @cache_control(max_age=7200, s_maxage=7200)
    def list(self, request):
        scraper = ZuZarautzPostScraper()
        data = scraper.get_data()

        return Response({
            "meta": {
                "language": "eu",
                "lastUpdated": scraper.updated,
                "source": scraper.get_source(),
                "totalCount": len(data)
            },
            'data': data
        })
