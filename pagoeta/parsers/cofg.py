import datetime

from typing import NamedTuple

from .base import JsonParser


DUTY_DAY = 0
DUTY_NIGHT = 1


class OnDutyPharmacy(NamedTuple):
    date: datetime.date
    duty: int
    id: int


class CofgParser(JsonParser):
    def parse(self, *, date: datetime.date, duty: int) -> OnDutyPharmacy:
        return OnDutyPharmacy(date, duty, int(self.json[0]['id']))
