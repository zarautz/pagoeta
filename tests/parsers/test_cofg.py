import os

from datetime import datetime
from unittest import TestCase

from pagoeta.parsers.cofg import OnDutyPharmacy, CofgParser, DUTY_DAY, DUTY_NIGHT


BASE_DIR = os.path.dirname(__file__)


class CofgParserDayTests(TestCase):
    @classmethod
    def setUpClass(self):
        self.date = datetime.today().date()

        with open(os.path.join(BASE_DIR, 'sources', 'cofg_day.json'), 'rb') as file:
            parser = CofgParser(source=file.read())
            self.data = parser.parse(date=self.date, duty=DUTY_DAY)

    def test_parser(self):
        self.assertEqual(self.data, OnDutyPharmacy(self.date, DUTY_DAY, 890))


class CofgParserNightTests(TestCase):
    @classmethod
    def setUpClass(self):
        self.date = datetime.today().date()

        with open(os.path.join(BASE_DIR, 'sources', 'cofg_night.json'), 'rb') as file:
            parser = CofgParser(source=file.read())
            self.data = parser.parse(date=self.date, duty=DUTY_NIGHT)

    def test_parser(self):
        self.assertEqual(self.data, OnDutyPharmacy(self.date, DUTY_NIGHT, 524))
