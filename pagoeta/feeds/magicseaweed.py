import datetime

from typing import Dict, List

from pagoeta.settings import MAGICSEAWEED_API_KEY
from .base import BaseFeed, JsonParser
from .typing import FeedRequest, FeedResponse


class MagicseaweedParser(JsonParser):
    def parse(self, *, dates: List[datetime.date]) -> Dict[datetime.date, dict]:
        data = {}
        date_str_list = [str(date) for date in dates]

        for element in self.json:
            date_str = datetime.datetime.fromtimestamp(element['localTimestamp']).strftime('%Y-%m-%d')

            if date_str in date_str_list:
                data[date_str] = {
                    'charts': element['charts'],
                    'wave': {
                        'rating': {
                            'solid': element['solidRating'],
                            'faded': element['fadedRating'],
                        },
                        'swell': element['swell'],
                    },
                    'weather': element['condition'],
                    'wind': element['wind'],
                }

        return data


class MagicseaweedFeed(BaseFeed):
    parser = MagicseaweedParser

    def prepare_requests(self) -> List[FeedRequest]:
        return [FeedRequest(
            f'http://magicseaweed.com/api/{MAGICSEAWEED_API_KEY}/forecast/?spot_id=1061&units=eu',
            {'dates': self.dates}
        )]

    def process_response(self, response: FeedResponse):
        return self.parser(content=response.content).parse(**response.config)
