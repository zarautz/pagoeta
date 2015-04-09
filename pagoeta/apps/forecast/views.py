from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, ReadOnlyModelViewSet

from .models import WeatherCode


class ForecastViewSet(ViewSet):
    """
    Get current forecast.
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def list(self, request):
        return Response({
            "meta": {
                "lastUpdated": "2015-04-07T19:36:59+0200",
                "source": {
                    "AEMET": "http://www.aemet.es",
                    "Gipuzkoako Foru Aldundia": "http://gipuzkoa.net"
                }
            },
            'data': None
        })


class WeatherCodeViewSet(ReadOnlyModelViewSet):
    """
    Get available weather codes (used in the forecast).
    """
    queryset = WeatherCode.objects.all()

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
