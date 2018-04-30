import datetime
import json

from lxml import etree
from typing import List

from .typing import FeedRequest, FeedResponse


class BaseFeed:
    parser = None

    def __init__(self, *, dates: List[datetime.date] = [], locale: str = 'eu') -> None:
        self.dates = dates
        self.locale = locale

    def prepare_requests(self) -> List[FeedRequest]:
        raise NotImplementedError

    def process_response(self, response: FeedResponse):
        raise NotImplementedError


class BaseParser:
    source_encoding = 'utf-8'

    def __init__(self, *, content) -> None:
        self.content = content

    def parse(self):
        raise NotImplementedError


class XmlParser(BaseParser):
    parser = None

    @property
    def tree(self):
        try:
            return etree.fromstring(self.content, parser=self.parser)
        except etree.XMLSyntaxError:
            raise Exception  # TODO: custom Exception


class HtmlParser(XmlParser):
    parser = etree.HTMLParser()


class RssFeedParser(XmlParser):
    pass


class JsonParser(BaseParser):
    @property
    def json(self):
        return json.loads(self.content)
