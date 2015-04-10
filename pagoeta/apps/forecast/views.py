from datetime import date, timedelta
from django.utils import timezone
from django.views.decorators.cache import cache_control
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, ReadOnlyModelViewSet

from .models import WeatherCode
from .scrapers import ForecastScraperWrapper


class ForecastViewSet(ViewSet):
    """
    Get current forecast: weather, tides and astronomy data.
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)

    @cache_control(max_age=7200, s_maxage=7200)
    def list(self, request):
        date_list = [date.today() + timedelta(days=x) for x in range(0, 7)]
        scraper = ForecastScraperWrapper(date_list)

        return Response({
            'meta': {
                'lastUpdated': timezone.now(),
                'source': scraper.get_source()
            },
            'data': scraper.get_data()
        })


class WeatherCodeViewSet(ReadOnlyModelViewSet):
    """
    Get available weather codes (used in the weather forecast).
    """
    queryset = WeatherCode.objects.all()

    @cache_control(max_age=7200, s_maxage=7200)
    def list(self, request):
        data = {}

        for item in WeatherCode.objects.all():
            data[item.code] = {
                'name': item.name
            }

        return Response({
            'meta': {
                'language': request.LANGUAGE_CODE,
                'totalCount': WeatherCode.objects.count()
            },
            'data': data
        })
