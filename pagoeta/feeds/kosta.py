import time

from typing import List, NamedTuple

from .base import BaseFeed, HtmlParser
from .typing import FeedRequest, FeedResponse


class KostaImages(NamedTuple):
    snapshots: List[str]
    timex: List[str]


class KostaParser(HtmlParser):
    def parse(self) -> KostaImages:
        output = KostaImages([], [])

        for img in self.tree.xpath('//a[@class="monitorizaciones"]/img'):
            src = f'{img.get("src")}?{time.time()}'
            if 'snap.jpeg' in src:
                output.snapshots.append(src)
            else:
                output.timex.append(src)

        return output


class KostaFeed(BaseFeed):
    parser = KostaParser

    def prepare_requests(self) -> List[FeedRequest]:
        return [FeedRequest('http://www.kostasystem.com/monitorizaciones/zarautz/')]

    def process_response(self, response: FeedResponse):
        return self.parser(content=response.content).parse()
