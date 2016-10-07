import json

from datetime import date, timedelta
from requests import post
from requests.exceptions import RequestException

from .models import Pharmacy
from pagoeta.apps.core.exceptions import ServiceUnavailableException
from pagoeta.apps.osm.scrapers import OpenStreeMapScraper
from pagoeta.apps.places.models import Place
from pagoeta.apps.places.serializers import PlaceListSerializer


class PharmacyGuardScraper(object):
    temp = []
    place_ids = []

    def __init__(self, **kwargs):
        self.version = kwargs.get('version', 'v2')
        self.url = kwargs.get('url', 'http://m.cofgipuzkoa.com/ws/cofg_ws.php')

    def request_data_from_cofg(self, date, guard_time='day'):
        try:
            data = {
                'op': 'getPharmaciesGuard',
                'lang': 'eu',
                'month': date.month,
                'day': date.day,
                'guardtime': 0 if guard_time == 'day' else 1,
                'guardzone': 18,
            }

            return post(self.url, data=data)
        except RequestException:
            raise ServiceUnavailableException

    def get_source(self):
        return {'COFG': 'https://www.cofgipuzkoa.com/'}

    def get_data(self):
        return {
            'hours': self.get_hours(),
            'places': self.get_places(),
        }

    def get_hours(self):
        today = date.today()
        yesterday = today - timedelta(1)
        tomorrow = today + timedelta(1)

        night_shift_pharmacy_id = self.parse_pharmacy_id(today, 'night')

        return (
            {
                'date': str(today),
                '0000-0859': self.parse_pharmacy_id(yesterday, 'night'),
                '0900-2159': self.parse_pharmacy_id(today, 'day'),
                '2200-2359': night_shift_pharmacy_id,
            },
            {
                'date': str(tomorrow),
                '0000-0859': night_shift_pharmacy_id,
                '0900-2159': self.parse_pharmacy_id(tomorrow, 'day'),
                '2200-2359': self.parse_pharmacy_id(tomorrow, 'night'),
            },
        )

    def parse_pharmacy_id(self, date, guard_time='day', source=None):
        """JSON source can be passed for testing purposes."""
        if not source:
            request = self.request_data_from_cofg(date, guard_time)
            if request.status_code == 404:
                raise ServiceUnavailableException
            source = request.text

        cofg_pharmacy_id = int(json.loads(source)[0]['id'])
        pharmacy_id = self.get_internal_pharmacy_id(cofg_pharmacy_id)

        return pharmacy_id

    def get_internal_pharmacy_id(self, cofg_pharmacy_id):
        if self.version == 'v1':
            if not self.temp:
                self.temp = list(Pharmacy.objects.all())

            pharmacy = [el for el in self.temp if el.cofg_id == cofg_pharmacy_id][0]
            if pharmacy.place_id not in self.place_ids:
                self.place_ids.append(pharmacy.place_id)
            return pharmacy.place_id

        if self.version == 'v2':
            if not self.temp:
                self.temp = OpenStreeMapScraper().get_data()

            try:
                pharmacy = self.temp['nodes'][self.temp['index'][self.temp['pharmacies'][cofg_pharmacy_id]]]
                if pharmacy['id'] not in self.place_ids:
                    self.place_ids.append(self.temp['pharmacies'][cofg_pharmacy_id])
                return pharmacy['id']
            except:
                return None

    def get_places(self):
        places = {}

        if self.version == 'v1':
            for obj in Place.objects.filter(id__in=self.place_ids).prefetch_related('types', 'images').all():
                places[obj.id] = PlaceListSerializer(obj).data

        if self.version == 'v2':
            for pk in self.place_ids:
                try:
                    places[pk] = self.temp['nodes'][self.temp['index'][pk]]
                except:
                    places[pk] = None

        return places
