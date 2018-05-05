from typing import List

from pagoeta.feeds import GipuzkoaTidesFeed, KostaFeed, MagicseaweedFeed
from pagoeta.feeds.typing import FeedResponse
from .base import BaseSpider


class SeaSpider(BaseSpider):
    feed_classes = (GipuzkoaTidesFeed, KostaFeed, MagicseaweedFeed)

    def process_responses(self, responses: List[FeedResponse]):
        import datetime
        import json

        def default(obj):
            if isinstance(obj, (datetime.date, datetime.datetime)):
                return obj.isoformat()

        return json.dumps(responses, default=default)
