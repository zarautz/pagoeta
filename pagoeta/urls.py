from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers

from pagoeta.apps.core import views as core_views
from pagoeta.apps.events.views import EventViewSet
from pagoeta.apps.forecast.views import ForecastViewSet, WeatherCodeViewSet
from pagoeta.apps.health.views import PharmacyViewSet
from pagoeta.apps.places.views import PlaceViewSet, TypeViewSet as PlaceTypeViewSet
from pagoeta.apps.posts.views import ZuZarautzPostViewSet


# http://www.django-rest-framework.org/api-guide/routers/
router_v1 = routers.DefaultRouter()
router_v1.register(r'events', EventViewSet, base_name='event')
router_v1.register(r'forecast/weather/codes', WeatherCodeViewSet, base_name='weather-code')
router_v1.register(r'forecast', ForecastViewSet, base_name='forecast')
router_v1.register(r'pharmacies/duty', PharmacyViewSet, base_name='pharmacy')
router_v1.register(r'places/types', PlaceTypeViewSet, base_name='place-type')
router_v1.register(r'places', PlaceViewSet, base_name='place')
router_v1.register(r'posts/zuzarautz', ZuZarautzPostViewSet, base_name='zuzarautz-post')


urlpatterns = [
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^assets/ximg/(?P<filter>[\w-]+)/(?P<hash>[\w-]+).jpeg', core_views.XeroxView.as_view(), name='xerox'),
    url(r'^api/docs/', include('rest_framework_swagger.urls')),
    url(r'^v1/', include(router_v1.urls, namespace='v1')),
    url(r'^$', core_views.RedirectView.as_view(), name='redirect'),
]
