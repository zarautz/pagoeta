import datetime
import json

from typing import List, NamedTuple

from .base import BaseFeed, JsonParser
from .typing import FeedRequest, FeedResponse


DUTY_DAY = 0
DUTY_NIGHT = 1


class OnDutyPharmacy(NamedTuple):
    date: datetime.date
    duty: int
    id: int


class CofgParser(JsonParser):
    def parse(self, *, date: datetime.date, duty: int) -> OnDutyPharmacy:
        return OnDutyPharmacy(date, duty, int(self.json[0]['id']))


class CofgFeed(BaseFeed):
    parser = CofgParser

    def prepare_requests(self) -> List[FeedRequest]:
        reqs = []

        for duty in [DUTY_DAY, DUTY_NIGHT]:
            for date in self.dates:
                reqs.append(FeedRequest(
                    'http://m.cofgipuzkoa.com/ws/cofg_ws.php',
                    {'date': date, 'duty': duty},
                    'POST',
                    {
                        'op': 'getPharmaciesGuard',
                        'lang': 'eu',
                        'month': date.month,
                        'day': date.day,
                        'guardtime': duty,
                        'guardzone': 18,
                    }
                ))

        return reqs

    def process_responses(self, responses: List[FeedResponse]):
        test = [self.parser(content=res.content).parse(**res.config) for res in responses]

        def default(obj):
            if type(obj) is datetime.date or type(obj) is datetime.datetime:
                return obj.isoformat()

        return json.dumps(test, default=default)
