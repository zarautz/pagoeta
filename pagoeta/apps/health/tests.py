import os

from datetime import date
from django.core.urlresolvers import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from .models import Pharmacy
from .scrapers import PharmacyGuardScraper
from pagoeta.apps.core.exceptions import ServiceUnavailableException
from pagoeta.apps.osm.scrapers import OpenStreeMapScraper


class HealthTests(TestCase):
    fixtures = ['test_data.json']


class PharmacyViewSetV1Tests(HealthTests):
    def setUp(self):
        self.response = APIClient().get(reverse('v1:pharmacy-list'))

    def test_default_response(self):
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(self.response.data['data']['hours']), 2)
        for day in self.response.data['data']['hours']:
            self.assertEqual('0900-2159' in day, True)
            self.assertEqual('0000-0859' in day, True)
            self.assertEqual('2200-2359' in day, True)


class PharmacyViewSetV2Tests(PharmacyViewSetV1Tests):
    def setUp(self):
        self.response = APIClient().get(reverse('v2:pharmacy-list'))


class PharmacyGuardScraperV1Tests(HealthTests):
    def setUp(self):
        BASE_DIR = os.path.dirname(__file__)
        self.source_day = open(os.path.join(BASE_DIR, 'sources/cofg_day.json')).read()
        self.source_night = open(os.path.join(BASE_DIR, 'sources/cofg_night.json')).read()
        self.pharmacies_map = {}
        self.scraper = PharmacyGuardScraper(version='v1')
        for pharmacy in Pharmacy.objects.all():
            self.pharmacies_map[pharmacy.cofg_id] = pharmacy.place_id

    def test_source(self):
        self.assertEqual(len(self.scraper.get_source().keys()), 1)

    def test_day(self):
        pharmacy_id = self.scraper.parse_pharmacy_id(None, None, self.source_day)
        self.assertEqual(pharmacy_id, self.pharmacies_map[890])

    def test_night(self):
        pharmacy_id = self.scraper.parse_pharmacy_id(None, None, self.source_night)
        self.assertEqual(pharmacy_id, self.pharmacies_map[524])


class PharmacyGuardScraperV2Tests(TestCase):
    def setUp(self):
        self.scraper = PharmacyGuardScraper(version='v2')

    def test_source(self):
        self.assertEqual(len(self.scraper.get_source().keys()), 2)

    def test_parser(self):
        osm_data = OpenStreeMapScraper().get_data()
        pharmacies = dict((v, k) for k, v in osm_data['pharmacies'].iteritems())
        cofg_data = self.scraper.get_data()
        for key in cofg_data['places'].keys():
            self.assertTrue(key in pharmacies)

    def test_unknown_cofg_id(self):
        self.assertEqual(self.scraper.get_internal_pharmacy_id(0), None)


class PharmacyGuardScraper404Tests(TestCase):
    def test_404_request(self):
        scraper = PharmacyGuardScraper(url='http://m.cofgipuzkoa.com/ws/missing.php')
        self.assertRaises(ServiceUnavailableException, scraper.parse_pharmacy_id, date.today())
