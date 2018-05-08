from typing import List, NamedTuple
from urllib.parse import urlencode

from pagoeta.settings import ZARAUTZ_BBOX
from .base import BaseFeed, JsonParser
from .typing import FeedRequest, FeedResponse


class Place(NamedTuple):
    id: int
    name: str


class OverpassParser(JsonParser):
    def parse(self) -> dict:
        return self.data


class OverpassFeed(BaseFeed):
    parser = OverpassParser
    features = [
        ('amenity', ['bench', 'telephone']),
        ('craft', []),
        ('historic', []),
        ('leisure', ['common', 'slipway']),
        ('public_transport', []),
        ('shop', []),
        ('sport', []),
        ('tourism', [])
    ]

    def __init__(self, *, types: List[str] = []) -> None:
        self.types = types

    def prepare_requests(self) -> List[FeedRequest]:
        nodes = ';'.join(
            ['node[%s]%s' % (f[0], ''.join(['[%s!=%s]' % (f[0], n) for n in f[1]])) for f in self.features]
        )
        ways = ';'.join(
            ['way[%s]%s' % (f[0], ''.join(['[%s!=%s]' % (f[0], n) for n in f[1]])) for f in self.features]
        )
        query = f'[out:json][bbox:{ZARAUTZ_BBOX}];({nodes};{ways};);out;'
        url = f'http://overpass-api.de/api/interpreter?{urlencode({"data": query})}'

        return [FeedRequest(
            url
        )]

    def process_response(self, response: FeedResponse):
        elements = self.parser(content=response.content).parse()['elements']
        features = list(dict(self.features).keys())

        output = {
            'elements': {},
            'features': {},
        }

        for el in elements:
            for feat in features:
                if feat in el['tags']:
                    el['type'] = f'{feat}:{el["tags"][feat]}'
                    break

            if el['type'] not in output['features']:
                output['features'][el['type']] = {
                    'elements': [el['id']],
                    'href': None,
                    'url': f"http://wiki.openstreetmap.org/wiki/Tag:{el['type'].replace(':', '=')}",
                }
            else:
                output['features'][el['type']]['elements'].append(el['id'])

            output['elements'][el['id']] = el

        if self.types:
            return [{
                feature: [output['elements'][el] for el in output['features'][feature]['elements']]
            } for feature in self.types]

        return output
