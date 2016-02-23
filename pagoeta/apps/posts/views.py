from django.views.decorators.cache import cache_control
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .scrapers import ZuZarautzPostScraper, HitzaPostScraper


class BasePostViewSet(ViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    scraper = None

    def list(self, request):
        scraper = self.scraper
        data = scraper.get_data()

        return Response({
            'meta': {
                'language': scraper.language,
                'lastUpdated': scraper.updated,
                'source': scraper.get_source(),
                'totalCount': len(data),
            },
            'data': data,
        })


class HitzaPostViewSet(BasePostViewSet):
    scraper = HitzaPostScraper()

    @cache_control(max_age=3600)
    def list(self, request):
        """
        Get the latest Zarauzko Hitza news (language="eu").
        """
        return super(HitzaPostViewSet, self).list(request)


class ZuZarautzPostViewSet(BasePostViewSet):
    scraper = ZuZarautzPostScraper()

    @cache_control(max_age=10800)
    def list(self, request):
        """
        Get the latest Zu Zarautz news (language="eu").
        """
        return super(ZuZarautzPostViewSet, self).list(request)
