import os

from unittest import TestCase

from pagoeta.feeds.kosta import KostaParser


BASE_DIR = os.path.dirname(__file__)


class IngurumenaParserTests(TestCase):
    @classmethod
    def setUpClass(self):
        with open(os.path.join(BASE_DIR, 'sources', 'kosta.html'), 'rb') as file:
            parser = KostaParser(content=file.read())
            self.data = parser.parse()

    def test_parse(self):
        self.assertEqual(len(self.data.snapshots), 2)
        self.assertEqual(len(self.data.timex), 3)
        self.assertTrue('snap.jpeg?' in self.data.snapshots[0])
        self.assertTrue('timex.jpeg?' in self.data.timex[0])
