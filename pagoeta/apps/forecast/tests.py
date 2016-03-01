import os

from datetime import datetime
from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from .models import WeatherCode
from .scrapers import TideScraper, WaveScraper, WeatherScraper


class ForecastViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('v1:forecast-list')

    def test_default_response(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class WeatherCodeViewSetTests(TestCase):
    fixtures = ['test_data.json']

    def setUp(self):
        self.client = APIClient()
        self.weather_codes_count = WeatherCode.objects.count()
        self.url = reverse('v1:weather-code-list')

    def test_default_response(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['meta']['language'], settings.LANGUAGE_CODE)
        self.assertEqual(len(response.data['data']), self.weather_codes_count)


class TideScraperTests(TestCase):
    def setUp(self):
        BASE_DIR = os.path.dirname(__file__)
        self.date = datetime.strptime('2015-04-20', '%Y-%m-%d').date()
        self.date_one_high = datetime.strptime('2015-04-13', '%Y-%m-%d').date()
        self.date_one_low = datetime.strptime('2015-04-19', '%Y-%m-%d').date()
        self.scraper = TideScraper([self.date, self.date_one_high, self.date_one_low])
        self.source = open(os.path.join(BASE_DIR, 'sources/gipuzkoa.html')).read()

    def test_parse_html(self):
        data = self.scraper.parse_html(None, self.source)
        self.assertEqual(data[str(self.date)], {'high': ['06:19', '18:39'], 'low': ['00:00', '12:22']})
        self.assertEqual(data[str(self.date_one_high)], {'high': ['12:26'], 'low': ['05:59', '18:30']})
        self.assertEqual(data[str(self.date_one_low)], {'high': ['05:35', '17:56'], 'low': ['11:39']})


class WaveScraperTests(TestCase):
    def setUp(self):
        BASE_DIR = os.path.dirname(__file__)
        self.date = datetime.strptime('2013-04-25', '%Y-%m-%d').date()
        self.scraper = WaveScraper([self.date])
        self.source = open(os.path.join(BASE_DIR, 'sources/magicseaweed.json')).read()

    def test_parse_json(self):
        data = self.scraper.parse_json(self.source)
        self.assertEqual(data[str(self.date)], {
            'charts': {
                'swell': 'http://cdn.magicseaweed.com/wave/750/1-1366902000-1.gif',
                'period': 'http://cdn.magicseaweed.com/wave/750/1-1366902000-2.gif',
                'wind': 'http://cdn.magicseaweed.com/gfs/750/1-1366902000-4.gif',
                'pressure': 'http://cdn.magicseaweed.com/gfs/750/1-1366902000-3.gif',
                'sst': 'http://cdn.magicseaweed.com/sst/750/1-1366902000-10.gif'
            },
            'wave': {
                'rating': {
                    'faded': 0,
                    'solid': 0,
                },
                'swell': {
                    'minBreakingHeight': 1,
                    'absMinBreakingHeight': 1.06,
                    'maxBreakingHeight': 2,
                    'absMaxBreakingHeight': 1.66,
                    'unit': 'ft',
                    'components': {
                        'combined': {
                            'height': 1.1,
                            'period': 14,
                            'direction': 93.25,
                            'compassDirection': 'W'
                        },
                        'primary': {
                            'height': 1,
                            'period': 7,
                            'direction': 83.37,
                            'compassDirection': 'W'
                        },
                        'secondary': {
                            'height': 0.4,
                            'period': 9,
                            'direction': 92.32,
                            'compassDirection': 'W'
                        },
                        'tertiary': {
                            'height': 0.3,
                            'period': 13,
                            'direction': 94.47,
                            'compassDirection': 'W'
                         }
                     }
                },
            },
            'weather': {
                'pressure': 1020,
                'temperature': 18,
                'unitPressure': 'mb',
                'unit': 'c'
            },
            'wind': {
                'speed': 10,
                'direction': 85,
                'compassDirection': 'W',
                'chill': 15,
                'gusts': 13,
                'unit': 'mph'
            },
        })


class WeatherScraperTests(TestCase):
    def setUp(self):
        BASE_DIR = os.path.dirname(__file__)
        self.date = datetime.strptime('2015-04-21', '%Y-%m-%d').date()
        self.date_some_periods = datetime.strptime('2015-04-20', '%Y-%m-%d').date()
        self.date_two_periods = datetime.strptime('2015-04-23', '%Y-%m-%d').date()
        self.date_no_periods = datetime.strptime('2015-04-26', '%Y-%m-%d').date()
        self.scraper = WeatherScraper([self.date, self.date_some_periods, self.date_two_periods, self.date_no_periods])
        self.source = open(os.path.join(BASE_DIR, 'sources/aemet.xml')).read()
        self.data = self.scraper.parse_xml(self.source)

    def test_parse_xml(self):
        data = self.data[str(self.date)]
        self.assertEqual(len(data['forecast']), 4)
        self.assertEqual(data, {
            'tempMin': 11,
            'tempMax': 20,
            'uvMax': 6,
            'forecast': [
                {
                    'period': '00-06',
                    'code': 12,
                    'precipitationProb': 0,
                    'windDirection': 'C',
                    'windSpeed': 0,
                },
                {
                    'period': '06-12',
                    'code': 12,
                    'precipitationProb': 0,
                    'windDirection': 'NE',
                    'windSpeed': 10,
                },
                {
                    'period': '12-18',
                    'code': 12,
                    'precipitationProb': 0,
                    'windDirection': 'C',
                    'windSpeed': 0,
                },
                {
                    'period': '18-24',
                    'code': 15,
                    'precipitationProb': 0,
                    'windDirection': 'SE',
                    'windSpeed': 20,
                }
            ],
        })

    def test_parse_xml_some_periods(self):
        data = self.data[str(self.date_some_periods)]
        self.assertEqual(len(data['forecast']), 3)
        self.assertEqual(data, {
            'tempMin': 10,
            'tempMax': 15,
            'uvMax': 6,
            'forecast': [
                {
                    'period': '06-12',
                    'code': 11,
                    'precipitationProb': 0,
                    'windDirection': 'NE',
                    'windSpeed': 15,
                },
                {
                    'period': '12-18',
                    'code': 11,
                    'precipitationProb': 0,
                    'windDirection': 'NE',
                    'windSpeed': 10,
                },
                {
                    'period': '18-24',
                    'code': 11,
                    'precipitationProb': 0,
                    'windDirection': 'C',
                    'windSpeed': 0,
                }
            ],
        })

    def test_parse_xml_two_periods(self):
        data = self.data[str(self.date_two_periods)]
        self.assertEqual(len(data['forecast']), 2)
        self.assertEqual(data, {
            'tempMin': 8,
            'tempMax': 16,
            'uvMax': 6,
            'forecast': [
                {
                    'period': '00-12',
                    'code': 45,
                    'precipitationProb': 70,
                    'windDirection': 'W',
                    'windSpeed': 20,
                },
                {
                    'period': '12-24',
                    'code': 15,
                    'precipitationProb': 5,
                    'windDirection': 'NW',
                    'windSpeed': 10,
                }
            ],
        })

    def test_parse_xml_no_periods(self):
        data = self.data[str(self.date_no_periods)]
        self.assertEqual(len(data['forecast']), 1)
        self.assertEqual(data, {
            'tempMin': None,
            'tempMax': None,
            'uvMax': None,
            'forecast': [
                {
                    'period': '00-24',
                    'code': 24,
                    'precipitationProb': 100,
                    'windDirection': 'W',
                    'windSpeed': 5,
                }
            ],
        })
