from rest_framework.routers import DefaultRouter

from pagoeta.apps.events.views import EventViewSet
from pagoeta.apps.forecast.views import ForecastViewSet, WeatherCodeViewSet
from pagoeta.apps.health.views import PharmacyViewSet
from pagoeta.apps.osm.views import ElementViewSet, FeatureViewSet
from pagoeta.apps.places.views import PlaceViewSet, TypeViewSet as PlaceTypeViewSet
from pagoeta.apps.posts.views import HitzaPostViewSet, ZuZarautzPostViewSet


class Router(DefaultRouter):
    def __init__(self, version='v2'):
        super(self.__class__, self).__init__()

        self.register(r'forecast/weather/codes', WeatherCodeViewSet, base_name='weather-code')
        self.register(r'forecast', ForecastViewSet, base_name='forecast')

        if version == 'v1':
            self.register(r'events', EventViewSet, base_name='event')
            self.register(r'pharmacies/duty', PharmacyViewSet, base_name='pharmacy')
            self.register(r'places/types', PlaceTypeViewSet, base_name='place-type')
            self.register(r'places', PlaceViewSet, base_name='place')
            self.register(r'posts/zuzarautz', ZuZarautzPostViewSet, base_name='zuzarautz-post')

        if version == 'v2':
            self.register(r'health/pharmacies/duty', PharmacyViewSet, base_name='pharmacy')
            self.register(r'places/types', FeatureViewSet, base_name='osm-feature')
            self.register(r'places', ElementViewSet, base_name='osm-element')
            self.register(r'posts/hitza', HitzaPostViewSet, base_name='hitza-post')
