from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase
from PIL import Image
from rest_framework import status
from rest_framework.test import APIClient
from StringIO import StringIO

from .functions import IMAGE_SIZES, get_absolute_uri
from .helpers import XeroxMachine
from .serializers import ImageField
from pagoeta.apps.places.tests import PlaceTests


class ImageDummyObject(object):
    is_featured = True

    def get_sources(self):
        return {}


class ImageFieldTests(TestCase):
    def test_representation(self):
        obj = ImageDummyObject()
        self.assertEqual(
            {'source': obj.get_sources(), 'isFeatured': obj.is_featured},
            ImageField(read_only=True).to_representation(obj)
        )


class LanguageOnQueryParamMiddlewareTests(PlaceTests):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('v1:place-type-list')

    def test_default_language(self):
        response = self.client.get(self.url)
        self.assertEqual(response.data['meta']['language'], settings.LANGUAGE_CODE)

    def test_available_language(self):
        language = 'es'
        response = self.client.get(self.url, {'language': language})
        self.assertEqual(response.data['meta']['language'], language)

    def test_language_non_existent(self):
        response = self.client.get(self.url, {'language': 'xx'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_language_in_admin(self):
        response = self.client.get('/admin/', {'language': 'es'})
        self.assertEqual(response['Content-Language'], 'eu')


class RedirectViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_redirect(self):
        response = self.client.get('/')
        self.assertRedirects(response, reverse('django.swagger.base.view'), status_code=301)


class XeroxViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.sizes = ('q', 'n')
        self.urls = {}
        self.nurls = {}
        x_hash = XeroxMachine().add('http://www.google.com/google.jpg')
        no_hash = XeroxMachine().add('http://zarautz.xyz/open.jpg')
        for size in self.sizes:
            self.urls[size] = get_absolute_uri(reverse('image', args=(XeroxMachine.IMAGE_TYPE_IN_URL, x_hash, size)))
            self.nurls[size] = get_absolute_uri(reverse('image', args=(XeroxMachine.IMAGE_TYPE_IN_URL, no_hash, size)))

    def test_default_response(self):
        response = self.client.get(self.urls[self.sizes[0]])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], 'image/jpeg')
        self.assertEqual(response['Cache-Control'], 'max-age=604800')

    def test_no_response(self):
        response = self.client.get(self.nurls[self.sizes[0]])
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_no_event_response(self):
        response = self.client.get(self.urls[self.sizes[0]].replace('/x/', '/e/'))  # EventImage
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_no_place_response(self):
        response = self.client.get(self.urls[self.sizes[0]].replace('/x/', '/p/'))  # PlaceImage
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_image_sizes(self):
        for size in self.sizes:
            image = Image.open(StringIO(self.client.get(self.urls[size]).content))
            self.assertEqual(image.size[0], IMAGE_SIZES[size]['size'][0])
