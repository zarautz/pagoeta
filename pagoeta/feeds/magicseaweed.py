import datetime

from typing import Dict, List

from pagoeta.settings import MAGICSEAWEED_API_KEY
from .base import BaseFeed, JsonParser
from .typing import FeedRequest, FeedResponse


class MagicseaweedParser(JsonParser):
    def parse(self, *, dates: List[datetime.date]) -> Dict[str, dict]:
        data = {}

        for element in self.data:
            date = datetime.datetime.fromtimestamp(element['localTimestamp']).date()
            if date in dates:
                data[str(date)] = element

        return data


class MagicseaweedFeed(BaseFeed):
    parser = MagicseaweedParser

    def __init__(self, *, dates: List[datetime.date] = []) -> None:
        self.dates = dates

    def prepare_requests(self) -> List[FeedRequest]:
        return [FeedRequest(
            f'http://magicseaweed.com/api/{MAGICSEAWEED_API_KEY}/forecast/?spot_id=1061&units=eu',
            {'dates': self.dates}
        )]

    def process_response(self, response: FeedResponse):
        return self.parser(content=response.content).parse(**response.config)
