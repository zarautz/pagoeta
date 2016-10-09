from collections import OrderedDict
from django.conf import settings
from django.core.cache import cache
from django.utils import timezone
from geojson import Point
from requests import get
from requests.exceptions import RequestException
from rest_framework.reverse import reverse
from urllib import urlencode

from pagoeta.apps.core.exceptions import ServiceUnavailableException
from pagoeta.apps.core.functions import get_absolute_uri


class OpenStreeMapScraper(object):
    """This is our filter. Full list is here: https://wiki.openstreetmap.org/wiki/Map_Features"""
    """The second list in every tuple is used to ignore some types inside a feature."""
    source = {'OpenStreetMap': 'https://www.openstreetmap.org/'}
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
    data = {}

    def __init__(self):
        self.data = self.get_data()

    def get_source(self, element=None):
        if element:
            el_type = 'way' if 'way' in element else 'node'
            return {'OpenStreetMap':  'https://www.openstreetmap.org/%s/%s' % (el_type, element['id'])}
        return self.source

    def request_data_from_osm(self):
        try:
            nodes = ';'.join(
                ['node[%s]%s' % (f[0], ''.join(['[%s!=%s]' % (f[0], n) for n in f[1]])) for f in self.features]
            )
            ways = ';'.join(
                ['way[%s]%s' % (f[0], ''.join(['[%s!=%s]' % (f[0], n) for n in f[1]])) for f in self.features]
            )
            query = '[out:json][bbox:%s];(%s;%s);out center;' % (settings.ZARAUTZ_BBOX, nodes, ways)
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

            """Get a 'reusable' url for elements."""
            base_href = get_absolute_uri(reverse('v2:osm-node-detail', ['1237'])).replace('/1237/', '/%s/')
            types_href = get_absolute_uri(reverse('v2:osm-node-list'))

            """Massage Overpass response before saving it in the cache."""
            data = {
                'updated_at': timezone.now(),
                'features': {},
                'elements': [],
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

                # Check coordinates. Ways will have a `center` attribute.
                if 'center' in el:
                    el['way'], el['lat'], el['lon'] = True, el['center']['lat'], el['center']['lon']
                    del el['center'], el['nodes']
                el['geometry'] = Point([el['lon'], el['lat']])
                del el['lat'], el['lon']

                el['href'] = base_href % el['id']

                if el['type'] not in data['features']:
                    data['features'][el['type']] = OrderedDict(sorted({
                        'count': 1,
                        'elements': [el['id']],
                        'href': '%s?types=%s' % (types_href, el['type']),
                        'url': 'http://wiki.openstreetmap.org/wiki/Tag:%s' % el['type'].replace(':', '='),
                    }.items()))
                else:
                    data['features'][el['type']]['count'] += 1
                    data['features'][el['type']]['elements'].append(el['id'])

                # Order data for a nicer presentation
                el['tags'] = OrderedDict(sorted(el['tags'].items()))
                el = OrderedDict(sorted(el.items()))

                data['elements'].append(el)
                data['index'][el['id']] = len(data['elements']) - 1

            cache.set(cache_key, data, cache_ttl)

        return data

    def get_features(self):
        return self.data['features']

    def get_elements(self, types_filter=None):
        if types_filter:
            output = []
            try:
                for tf in types_filter:
                    for node_id in self.data['features'][tf]['elements']:
                        output.append(self.data['elements'][self.data['index'][node_id]])
            except:
                pass

            return output

        return self.data['elements']

    def get_element(self, id):
        node = self.data['elements'][self.data['index'][int(id)]]
        del node['href']
        return node
