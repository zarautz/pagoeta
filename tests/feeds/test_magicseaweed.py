import os

from datetime import datetime
from unittest import TestCase

from pagoeta.feeds.magicseaweed import MagicseaweedParser


BASE_DIR = os.path.dirname(__file__)


class MagicseaweedParserTests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.date = datetime.strptime('2013-04-25', '%Y-%m-%d').date()

        with open(os.path.join(BASE_DIR, 'sources', 'magicseaweed.json'), 'rb') as file:
            parser = MagicseaweedParser(content=file.read())
            cls.data = parser.parse(dates=[cls.date])

    def test_parse(self):
        self.assertEqual(len(self.data[str(self.date)]), 9)
