from django.utils import timezone
from django.views.decorators.cache import cache_control
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .scrapers import PharmacyGuardScraper


class PharmacyViewSet(ViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    @cache_control(max_age=14400, s_maxage=14400)
    def list(self, request):
        """
        Get information about pharmacies on duty today and tomorrow.
        The corresponding Places (pharmacies) are included in the response.
        ---
        parameters:
        -   name: language
            paramType: query
            type: string
            description: ISO 639-1 language code.
            enum: [eu, es, en, fr]
            defaultValue: eu
        """
        scraper = PharmacyGuardScraper()

        return Response({
            'meta': {
                'language': request.LANGUAGE_CODE,
                'lastUpdated': timezone.now(),
                'source': scraper.get_source(),
            },
            'data': scraper.get_data(),
        })
