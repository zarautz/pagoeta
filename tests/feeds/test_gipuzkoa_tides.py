import os

from datetime import datetime
from unittest import TestCase

from pagoeta.feeds.gipuzkoa_tides import TideTable, GipuzkoaTidesParser


BASE_DIR = os.path.dirname(__file__)


class GipuzkoaTidesParserTests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.date = datetime.strptime('2016-10-10', '%Y-%m-%d').date()
        cls.date_one_low = datetime.strptime('2016-10-20', '%Y-%m-%d').date()
        cls.date_one_high = datetime.strptime('2016-10-25', '%Y-%m-%d').date()

        with open(os.path.join(BASE_DIR, 'sources', 'ingurumena_tides.html'), 'rb') as file:
            parser = GipuzkoaTidesParser(content=file.read())
            cls.data = parser.parse(dates=[cls.date, cls.date_one_high, cls.date_one_low])

    def test_parse(self):
        self.assertEqual(self.data[0], TideTable(self.date, ['04:36', '17:35'], ['11:12', '00:09']))
        self.assertEqual(self.data[1], TideTable(self.date_one_low, ['13:13'], ['07:00', '19:34']))
        self.assertEqual(self.data[2], TideTable(self.date_one_high, ['06:33', '19:18'], ['13:05']))
