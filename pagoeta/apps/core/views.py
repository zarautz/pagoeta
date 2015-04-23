from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.views import generic
from django.views.decorators.cache import cache_control
from PIL import Image
from requests import get
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import status
from StringIO import StringIO

from .functions import resize_image
from .models import XeroxImage
from pagoeta.apps.events.models import Image as EventImage
from pagoeta.apps.places.models import Image as PlaceImage


class RedirectView(generic.View):
    """
    Redirects to current API version.
    """
    def dispatch(self, request, *args, **kwargs):
        return redirect(reverse('django.swagger.base.view'))


class ImageView(generic.View):
    """
    Serves dinamically generated images.
    Images are taken directly from the source and then transformations are made.
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)

    @cache_control(max_age=31536000, s_maxage=31536000)
    def get(self, request, *args, **kwargs):
        source = kwargs.get('source')

        try:
            if source == 'e':
                image_url = EventImage.objects.get(hash=kwargs.get('hash')).get_url()
            elif source == 'p':
                image_url = PlaceImage.objects.get(hash=kwargs.get('hash')).get_url()
            elif source == 'x':
                image_url = XeroxImage.objects.get(hash=kwargs.get('hash')).url

        except ObjectDoesNotExist:
            return JsonResponse({'detail': 'Not Found.'}, status=status.HTTP_404_NOT_FOUND)

        image = Image.open(StringIO(get(image_url).content))
        image = resize_image(image, kwargs.get('size'))

        response = HttpResponse(content_type='image/jpeg')
        image.save(response, 'jpeg')

        return response
