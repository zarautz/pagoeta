from django.views.decorators.cache import cache_control
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, ReadOnlyModelViewSet

from .scrapers import PharmacyGuardScraper


class PharmacyViewSet(ViewSet):
    """
    Get information about pharmacies on duty today and tomorrow.
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)

    @cache_control(max_age=7200, s_maxage=7200)
    def list(self, request):
        scraper = PharmacyGuardScraper()

        return Response({
            "meta": {
                "lastUpdated": None,
                "source": scraper.get_source()
            },
            'data': scraper.get_data()
        })
