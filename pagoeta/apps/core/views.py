from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views import generic
from PIL import Image
from requests import get
from StringIO import StringIO

from .functions import resize_image
from .models import XeroxImage


class RedirectView(generic.View):
    """
    Redirects to current API version.
    """
    def dispatch(self, request, *args, **kwargs):
        return redirect(reverse('v1:api-root'))


class XeroxView(generic.View):
    """
    Serves dinamically generated images.
    Images are taken directly from the source and then transformations are made.
    """
    def get(self, request, *args, **kwargs):
        ximg = XeroxImage.objects.get(hash=kwargs.get('hash'))
        image = Image.open(StringIO(get(ximg.url).content))
        image = resize_image(image, kwargs.get('filter'))

        response = HttpResponse(content_type='image/jpeg')
        response['Cache-Control'] = 'public, max-age=31536000, s-maxage=31536000'
        image.save(response, 'jpeg')

        return response
