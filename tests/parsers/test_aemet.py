import os

from datetime import datetime
from unittest import TestCase

from pagoeta.parsers.aemet import AemetParser


BASE_DIR = os.path.dirname(__file__)


class MagicseaweedParserTests(TestCase):
    @classmethod
    def setUpClass(self):
        self.date = datetime.strptime('2015-04-21', '%Y-%m-%d').date()
        self.date_some_periods = datetime.strptime('2015-04-20', '%Y-%m-%d').date()
        self.date_two_periods = datetime.strptime('2015-04-23', '%Y-%m-%d').date()
        self.date_no_periods = datetime.strptime('2015-04-26', '%Y-%m-%d').date()

        with open(os.path.join(BASE_DIR, 'sources', 'aemet.xml'), 'rb') as file:
            parser = AemetParser(source=file.read())
            self.data = parser.parse(
                dates=[self.date, self.date_some_periods, self.date_two_periods, self.date_no_periods]
            )

    def test_parse(self):
        data = self.data[str(self.date)]
        self.assertEqual(len(data['forecast']), 4)
        self.assertEqual(data, {
            'temp_min': 11,
            'temp_max': 20,
            'uv_max': 6,
            'forecast': [
                {
                    'period': '00-06',
                    'code': 12,
                    'precipitation_prob': 0,
                    'wind_direction': 'C',
                    'wind_speed': 0,
                },
                {
                    'period': '06-12',
                    'code': 12,
                    'precipitation_prob': 0,
                    'wind_direction': 'NE',
                    'wind_speed': 10,
                },
                {
                    'period': '12-18',
                    'code': 12,
                    'precipitation_prob': 0,
                    'wind_direction': 'C',
                    'wind_speed': 0,
                },
                {
                    'period': '18-24',
                    'code': 15,
                    'precipitation_prob': 0,
                    'wind_direction': 'SE',
                    'wind_speed': 20,
                }
            ],
        })

    def test_parse_some_periods(self):
        data = self.data[str(self.date_some_periods)]
        self.assertEqual(len(data['forecast']), 3)
        self.assertEqual(data, {
            'temp_min': 10,
            'temp_max': 15,
            'uv_max': 6,
            'forecast': [
                {
                    'period': '06-12',
                    'code': 11,
                    'precipitation_prob': 0,
                    'wind_direction': 'NE',
                    'wind_speed': 15,
                },
                {
                    'period': '12-18',
                    'code': 11,
                    'precipitation_prob': 0,
                    'wind_direction': 'NE',
                    'wind_speed': 10,
                },
                {
                    'period': '18-24',
                    'code': 11,
                    'precipitation_prob': 0,
                    'wind_direction': 'C',
                    'wind_speed': 0,
                }
            ],
        })

    def test_parse_two_periods(self):
        data = self.data[str(self.date_two_periods)]
        self.assertEqual(len(data['forecast']), 2)
        self.assertEqual(data, {
            'temp_min': 8,
            'temp_max': 16,
            'uv_max': 6,
            'forecast': [
                {
                    'period': '00-12',
                    'code': 45,
                    'precipitation_prob': 70,
                    'wind_direction': 'W',
                    'wind_speed': 20,
                },
                {
                    'period': '12-24',
                    'code': 15,
                    'precipitation_prob': 5,
                    'wind_direction': 'NW',
                    'wind_speed': 10,
                }
            ],
        })

    def test_parse_no_periods(self):
        data = self.data[str(self.date_no_periods)]
        self.assertEqual(len(data['forecast']), 1)
        self.assertEqual(data, {
            'temp_min': None,
            'temp_max': None,
            'uv_max': None,
            'forecast': [
                {
                    'period': '00-24',
                    'code': 24,
                    'precipitation_prob': 100,
                    'wind_direction': 'W',
                    'wind_speed': 5,
                }
            ],
        })
