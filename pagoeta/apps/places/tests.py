from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from .models import Place, Type
from .views import PlaceViewSet


class PlaceViewSetListTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.visible_places_count = Place.objects.visible().count()
        self.url = reverse('v1:place-list')

    def test_default_response(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['meta']['offset'], 0)
        self.assertEqual(response.data['meta']['limit'], PlaceViewSet.DEFAULT_LIMIT)
        self.assertEqual(response.data['meta']['types'], None)
        self.assertEqual(response.data['meta']['totalCount'], self.visible_places_count)
        self.assertEqual(len(response.data['data']), self.visible_places_count)

    def test_parameters_offset_string(self):
        response = self.client.get(self.url, {'offset': 'zero'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_parameters_offset_negative(self):
        response = self.client.get(self.url, {'offset': -1})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_parameters_limit(self):
        limit = 1
        response = self.client.get(self.url, {'limit': limit})
        self.assertEqual(response.data['meta']['totalCount'], self.visible_places_count)
        self.assertEqual(len(response.data['data']), limit)

    def test_parameters_limit_string(self):
        response = self.client.get(self.url, {'limit': 'ten'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_parameters_limit_max(self):
        response = self.client.get(self.url, {'limit': PlaceViewSet.MAX_LIMIT + 1})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_parameters_types_one(self):
        response = self.client.get(self.url, {'types': 'one'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['meta']['types']['operator'], None)
        self.assertEqual(len(response.data['meta']['types']['filter']), 1)

    def test_parameters_types_or(self):
        response = self.client.get(self.url, {'types': 'one,two'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['meta']['types']['operator'], 'OR')
        self.assertEqual(len(response.data['meta']['types']['filter']), 2)

    def test_parameters_types_and(self):
        response = self.client.get(self.url, {'types': 'one+two+three'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['meta']['types']['operator'], 'AND')
        self.assertEqual(len(response.data['meta']['types']['filter']), 3)

    def test_parameters_types_mixed_operators(self):
        response = self.client.get(self.url, {'types': 'one,two+three'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class PlaceViewSetDetailTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.place = Place.objects.visible().first()
        self.invisible_place = Place.objects.filter(is_visible=False).first()
        self.url = reverse('v1:place-detail', args=(self.place.id,))
        self.invisible_url = reverse('v1:place-detail', args=(self.invisible_place.id,))

    def test_default_response(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invisible_place(self):
        response = self.client.get(self.invisible_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TypeViewSetListTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.place_types_count = Type.objects.count()
        self.url = reverse('v1:place-type-list')

    def test_default_response(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['meta']['language'], settings.LANGUAGE_CODE)
        self.assertEqual(len(response.data['data']), self.place_types_count)
