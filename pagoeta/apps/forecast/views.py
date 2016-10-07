from datetime import date, timedelta
from django.utils import timezone
from django.views.decorators.cache import cache_control
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .models import WeatherCode
from .scrapers import ForecastScraperWrapper


class ForecastViewSet(ViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    DAYS_FORECAST = 7

    @cache_control(max_age=7200)
    def list(self, request):
        """
        Get current forecast: weather, tides and astronomy data.
        """
        date_list = [date.today() + timedelta(days=x) for x in range(0, self.DAYS_FORECAST)]
        scraper = ForecastScraperWrapper(date_list, request.version)

        res = {
            'meta': {
                'lastUpdated': timezone.now(),
                'source': scraper.get_source(),
            },
            'data': scraper.get_data(),
        }

        if request.version == 'v2':
            res.update({'live': scraper.get_live_data()})

        return Response(res)


class WeatherCodeViewSet(ViewSet):
    queryset = WeatherCode.objects.all()

    @cache_control(max_age=86400)
    def list(self, request):
        """
        Get available weather codes (used in the weather forecast).
        ---
        parameters:
        -   name: language
            paramType: query
            type: string
            description: ISO 639-1 language code.
            enum: [eu, es, en, fr]
            defaultValue: eu
        """
        data = {}

        for item in WeatherCode.objects.all():
            data[item.code] = {
                'name': item.name,
            }

        return Response({
            'meta': {
                'language': request.LANGUAGE_CODE,
                'totalCount': len(data),
            },
            'data': data,
        })
