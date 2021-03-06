from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.utils.cache import patch_cache_control
from django.views import generic
from django.views.decorators.cache import cache_control
from rest_framework import status

from .functions import transform_external_image
from .helpers import XeroxMachine
from pagoeta.apps.events.models import Image as EventImage
from pagoeta.apps.places.models import Image as PlaceImage


class ImageView(generic.View):
    """
    Serves dinamically generated images.
    Images are taken directly from the source and then transformations are made.
    """
    @cache_control(max_age=31536000)
    def get(self, request, *args, **kwargs):
        cache_max_age = 31536000
        image_type = kwargs.get('image_type')
        image_hash = kwargs.get('hash')
        size = kwargs.get('size')

        not_found_response = JsonResponse({'detail': 'Not Found.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            if image_type == EventImage.IMAGE_TYPE_IN_URL:
                image_url = EventImage.objects.get(hash=image_hash).get_url()
            elif image_type == PlaceImage.IMAGE_TYPE_IN_URL:
                image_url = PlaceImage.objects.get(hash=image_hash).get_url()
            elif image_type == XeroxMachine.IMAGE_TYPE_IN_URL:
                image_url = XeroxMachine().get(image_hash)
                cache_max_age = 604800
        except ObjectDoesNotExist:
            return not_found_response

        try:
            image = transform_external_image(image_url, size)
            response = HttpResponse(content_type='image/jpeg')
            image.save(response, 'jpeg')
        except IOError:
            return not_found_response

        patch_cache_control(response, max_age=cache_max_age)

        return response
