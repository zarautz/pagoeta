from django.core.urlresolvers import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from .scrapers import OpenStreeMapScraper


class OpenStreeMapScraperTests(TestCase):
    def setUp(self):
        self.scraper = OpenStreeMapScraper()

    def test_get_source(self):
        dummy_node = {'id': 1}
        dummy_way = {'id': 1, 'way': True}
        self.assertEqual(self.scraper.source, self.scraper.get_source())
        self.assertTrue('/node/1' in self.scraper.get_source(dummy_node)['OpenStreetMap'])
        self.assertTrue('/way/1' in self.scraper.get_source(dummy_way)['OpenStreetMap'])


class ElementViewSetListTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('v2:osm-element-list')

    def test_default_response(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['meta']['types'], 'all')

    def test_parameters_types_one(self):
        response = self.client.get(self.url, {'types': 'shop:books'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['meta']['types']['filter']), 1)
        self.assertTrue('operator' not in response.data['meta']['types'])

    def test_parameters_types_or(self):
        response = self.client.get(self.url, {'types': 'amenity:pharmacy,shop:books'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['meta']['types']['filter']), 2)
        self.assertEqual(response.data['meta']['types']['operator'], 'OR')

    def test_parameters_types_invalid(self):
        response = self.client.get(self.url, {'types': 'invalid'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 0)


class ElementViewSetDetailTests(TestCase):
    def setUp(self):
        self.id = 1945635278
        self.client = APIClient()
        self.url = reverse('v2:osm-element-detail', args=(self.id,))

    def test_default_response(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['id'], self.id)
        self.assertEqual(response.data['data']['type'], 'shop:books')
        self.assertTrue('way' not in response.data['data'])


class FeatureViewSetListTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('v2:osm-feature-list')

    def test_default_response(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('shop:books' in response.data['data'])
