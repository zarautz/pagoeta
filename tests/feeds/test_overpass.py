import os

from unittest import TestCase

from pagoeta.feeds.overpass import OverpassParser


BASE_DIR = os.path.dirname(__file__)


class OverpassParserTests(TestCase):
    @classmethod
    def setUpClass(cls):
        with open(os.path.join(BASE_DIR, 'sources', 'overpass_places.json'), 'rb') as file:
            parser = OverpassParser(content=file.read())
            cls.data = parser.parse()

    def test_parse(self):
        self.skipTest('to-do')
