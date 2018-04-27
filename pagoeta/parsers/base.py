import datetime
import json

from lxml import etree
from typing import List


DateListType = List[datetime.date]


class BaseParser:
    source_encoding = 'utf-8'

    def __init__(self, *, source: str) -> None:
        self.source = source

    def parse(self):
        raise NotImplementedError


class XmlParser(BaseParser):
    parser = None

    @property
    def tree(self):
        try:
            return etree.fromstring(self.source, parser=self.parser)
        except etree.XMLSyntaxError:
            raise Exception  # TODO: custom Exception


class HtmlParser(XmlParser):
    parser = etree.HTMLParser()


class RssFeedParser(XmlParser):
    pass


class JsonParser(BaseParser):
    @property
    def json(self):
        return json.loads(self.source)
