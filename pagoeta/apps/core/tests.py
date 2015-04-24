from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase
from PIL import Image
from rest_framework import status
from rest_framework.test import APIClient
from StringIO import StringIO

from .functions import IMAGE_SIZES, get_absolute_uri
from .models import XeroxImage


class LanguageOnQueryParamMiddlewareTests(TestCase):
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
        self.assertRedirects(response, reverse('django.swagger.base.view'))


class XeroxViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.image = XeroxImage.objects.get(pk=1)
        self.sizes = ('q', 'n')
        self.urls = {}
        for size in self.sizes:
            self.urls[size] = get_absolute_uri(reverse('image', args=(XeroxImage.IMAGE_TYPE_IN_URL,
                                                                      self.image.hash, size)))

    def test_default_response(self):
        response = self.client.get(self.urls[self.sizes[0]])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], 'image/jpeg')

    def test_image_sizes(self):
        for size in self.sizes:
            image = Image.open(StringIO(self.client.get(self.urls[size]).content))
            self.assertEqual(image.size[0], IMAGE_SIZES[size]['size'][0])
