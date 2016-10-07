from django.conf import settings
from django.core.cache import cache
from django.utils import timezone
from geojson import Point
from requests import get
from requests.exceptions import RequestException
from urllib import urlencode

from pagoeta.apps.core.exceptions import ServiceUnavailableException


class OpenStreeMapScraper(object):
    """This is our filter. Full list is here: https://wiki.openstreetmap.org/wiki/Map_Features"""
    """The second tuple is used to ignore some types inside a feature."""
    features = [
        ('amenity', ['bench', 'telephone']),
        ('craft', []),
        ('historic', []),
        ('leisure', ['slipway']),
        ('public_transport', []),
        ('shop', []),
        ('sport', []),
        ('tourism', [])
    ]

    def request_data_from_osm(self):
        try:
            nodes = ';'.join(
                ['node[%s]%s' % (f[0], ''.join(['[%s!=%s]' % (f[0], n) for n in f[1]])) for f in self.features]
            )
            query = '[out:json][bbox:%s];(%s;);out;' % (settings.ZARAUTZ_BBOX, nodes)
            url = 'http://overpass-api.de/api/interpreter?%s' % urlencode({'data': query})

            return get(url).json()
        except RequestException:
            raise ServiceUnavailableException

    def get_data(self):
        cache_key = 'osm-overpass'
        cache_ttl = 4 * 60 * 60
        data = cache.get(cache_key)

        if not data:
            fkeys = [feature[0] for feature in self.features]
            response = self.request_data_from_osm()

            """Massage Overpass response before saving it in the cache."""
            data = {
                'updated_at': timezone.now(),
                'features': {},
                'nodes': [],
                'index': {},
                'pharmacies': {},
            }

            for el in response['elements']:
                # Check for feature type
                for key in fkeys:
                    if key in el['tags']:
                        el['type'] = '%s:%s' % (key, el['tags'][key])
                        break

                # Check if it is a registered pharmacy
                if el['type'] == 'amenity:pharmacy' and 'cofg:id' in el['tags']:
                    data['pharmacies'][int(el['tags']['cofg:id'])] = el['id']

                el['geometry'] = Point([el['lon'], el['lat']])
                del el['lon'], el['lat']

                if el['type'] not in data['features']:
                    data['features'][el['type']] = {
                        'url': 'http://wiki.openstreetmap.org/wiki/Tag:%s' % el['type'].replace(':', '='),
                        'nodes': [el['id']],
                        'count': 1
                    }
                else:
                    data['features'][el['type']]['nodes'].append(el['id'])
                    data['features'][el['type']]['count'] = len(data['features'][el['type']]['nodes'])

                data['nodes'].append(el)
                data['index'][el['id']] = len(data['nodes']) - 1

            cache.set(cache_key, data, cache_ttl)

        return data

    def get_updated_at(self):
        data = self.get_data()
        return data['updated_at']

    def get_features(self):
        data = self.get_data()
        return data['features']

    def get_nodes(self, types_filter=None):
        data = self.get_data()

        if types_filter:
            output = []
            try:
                for tf in types_filter:
                    for node_id in data['features'][tf]['nodes']:
                        output.append(data['nodes'][data['index'][node_id]])
            except:
                pass

            return output

        return data['nodes']

    def get_node(self, id):
        data = self.get_data()
        return data['nodes'][data['index'][int(id)]]
