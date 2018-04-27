import os

from unittest import TestCase

from pagoeta.parsers.overpass import OverpassParser


BASE_DIR = os.path.dirname(__file__)


class OverpassParserTests(TestCase):
    @classmethod
    def setUpClass(self):
        with open(os.path.join(BASE_DIR, 'sources', 'overpass_places.json'), 'rb') as file:
            parser = OverpassParser(source=file.read())
            self.data = parser.parse()

    def test_parse(self):
        self.assertTrue(False)
