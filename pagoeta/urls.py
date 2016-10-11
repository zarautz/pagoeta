from django.conf.urls import url, include
from django.views.generic.base import RedirectView

from .routers import Router
from pagoeta.apps.core import views as core_views


urlpatterns = [
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^api/doc/', RedirectView.as_view(pattern_name='django.swagger.base.view', permanent=True),
        name='redirect_old_api_docs'),
    url(r'^img/(?P<image_type>[epx]+)/(?P<hash>[a-f0-9]{40})_(?P<size>[qnzb]+).jpg', core_views.ImageView.as_view(),
        name='image'),
    url(r'^v1/', include(Router('v1').urls, namespace='v1')),
    url(r'^v2/', include(Router('v2').urls, namespace='v2')),
    url(r'^$', RedirectView.as_view(pattern_name='django.swagger.base.view', permanent=True), name='redirect'),
]
