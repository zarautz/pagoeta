import os

from datetime import datetime
from unittest import TestCase

from pagoeta.parsers.gipuzkoa import GaoBulletin, GipuzkoaGaoParser


BASE_DIR = os.path.dirname(__file__)


class GipuzkoaGaoParserTests(TestCase):
    @classmethod
    def setUpClass(self):
        self.date = datetime.strptime('2018-04-16', '%Y-%m-%d').date()

        with open(os.path.join(BASE_DIR, 'sources', 'gipuzkoa_gao.html'), 'rb') as file:
            self.parser = GipuzkoaGaoParser(source=file.read())
            self.data = self.parser.parse(date=self.date)

    def test_parse(self):
        self.assertEqual(len(self.data), 2)
        self.assertEqual(self.data[0], GaoBulletin(
            self.date,
            'Zarauzko kirol klub eta elkarteei 2018. urtean diru-laguntzak emateko deialdia',
            'https://ssl4.gipuzkoa.net/euskera/gao/2018/04/16/e1802472.htm'
        ))
