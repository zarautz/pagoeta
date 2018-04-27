import os

from datetime import datetime
from unittest import TestCase

from pagoeta.parsers.magicseaweed import MagicseaweedParser


BASE_DIR = os.path.dirname(__file__)


class MagicseaweedParserTests(TestCase):
    @classmethod
    def setUpClass(self):
        self.date = datetime.strptime('2013-04-25', '%Y-%m-%d').date()

        with open(os.path.join(BASE_DIR, 'sources', 'magicseaweed.json'), 'rb') as file:
            parser = MagicseaweedParser(source=file.read())
            self.data = parser.parse(dates=[self.date])

    def test_parse(self):
        self.assertEqual(self.data[str(self.date)], {
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
