import os

from datetime import datetime
from unittest import TestCase

from pagoeta.feeds.gipuzkoa_gao import GaoBulletin, GipuzkoaGaoParser


BASE_DIR = os.path.dirname(__file__)


class GipuzkoaGaoParserTests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.date = datetime.strptime('2018-04-16', '%Y-%m-%d').date()

        with open(os.path.join(BASE_DIR, 'sources', 'gipuzkoa_gao.html'), 'rb') as file:
            cls.parser = GipuzkoaGaoParser(content=file.read())
            cls.data = cls.parser.parse(date=cls.date)

    def test_parse(self):
        self.assertEqual(len(self.data), 2)
        self.assertEqual(self.data[0], GaoBulletin(
            self.date,
            'Zarauzko kirol klub eta elkarteei 2018. urtean diru-laguntzak emateko deialdia',
            'https://ssl4.gipuzkoa.net/euskera/gao/2018/04/16/e1802472.htm'
        ))
