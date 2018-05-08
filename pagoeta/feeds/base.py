import json

from defusedxml.lxml import fromstring
from lxml.etree import HTMLParser, XMLParser, XMLSyntaxError
from typing import List

from .typing import FeedRequest, FeedResponse


class BaseFeed:
    parser = None

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
    parser = XMLParser(ns_clean=True)

    @property
    def tree(self):
        try:
            return fromstring(self.content, parser=self.parser)
        except XMLSyntaxError:
            raise Exception  # TODO: custom Exception

    def parse(self):
        raise NotImplementedError


class HtmlParser(XmlParser):
    parser = HTMLParser()

    def parse(self):
        raise NotImplementedError


class RssFeedParser(XmlParser):
    def parse(self):
        raise NotImplementedError


class JsonParser(BaseParser):
    @property
    def data(self):
        return json.loads(self.content)

    def parse(self):
        raise NotImplementedError
