import os

from datetime import date
from django.core.urlresolvers import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from .models import Pharmacy
from .scrapers import PharmacyGuardScraper
from pagoeta.apps.core.exceptions import ServiceUnavailableException


class PharmacyViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('v1:pharmacy-list')

    def test_default_response(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']['hours']), 2)
        for day in response.data['data']['hours']:
            self.assertEqual('0900-2159' in day, True)
            self.assertEqual('0000-0859' in day, True)
            self.assertEqual('2200-2359' in day, True)


class PharmacyGuardScraperTests(TestCase):
    def setUp(self):
        BASE_DIR = os.path.dirname(__file__)
        self.scraper = PharmacyGuardScraper()
        self.source_day = open(os.path.join(BASE_DIR, 'sources/cofg_day.json')).read()
        self.source_night = open(os.path.join(BASE_DIR, 'sources/cofg_night.json')).read()
        self.pharmacies_map = {}
        for pharmacy in Pharmacy.objects.all():
            self.pharmacies_map[pharmacy.cofg_id] = pharmacy.place_id

    def test_day(self):
        pharmacy_id = self.scraper.parse_pharmacy_id(None, None, self.source_day)
        self.assertEqual(pharmacy_id, self.pharmacies_map[890])

    def test_night(self):
        pharmacy_id = self.scraper.parse_pharmacy_id(None, None, self.source_night)
        self.assertEqual(pharmacy_id, self.pharmacies_map[524])

    def test_404_request(self):
        scraper = PharmacyGuardScraper('http://m.cofgipuzkoa.com/ws/missing.php')
        self.assertRaises(ServiceUnavailableException, scraper.parse_pharmacy_id, date.today())
