from django.utils import timezone
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

    @cache_control(max_age=14400, s_maxage=14400)
    def list(self, request):
        scraper = PharmacyGuardScraper()

        return Response({
            "meta": {
                "lastUpdated": timezone.now(),
                "source": scraper.get_source()
            },
            'data': scraper.get_data()
        })
