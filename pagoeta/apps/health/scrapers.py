import json

from datetime import date, timedelta
from requests import post
from requests.exceptions import RequestException

from .models import Pharmacy
from pagoeta.apps.places.models import Place
from pagoeta.apps.places.serializers import PlaceListSerializer


class PharmacyGuardScraper():
    pharmacies = []
    place_ids = []

    def get_source(self):
        return { 'COFG': 'https://www.cofgipuzkoa.com/' }

    def get_data(self):
        return {
            'hours': self.get_hours(),
            'places': self.get_places(),
        }

    def get_places(self):
        places = {}
        for obj in Place.objects.filter(id__in=self.place_ids).prefetch_related('types', 'events').all():
            places[obj.id] = PlaceListSerializer(obj).data

        return places

    def get_hours(self):
        today = date.today()
        yesterday = today - timedelta(1)
        tomorrow = today + timedelta(1)

        return (
            {
                'date': str(today),
                '0000-0859': self.parse_pharmacy_id(yesterday, 'night'),
                '0900-2159': self.parse_pharmacy_id(today, 'day'),
                '2200-2359': self.parse_pharmacy_id(today, 'night'),
            },
            {
                'date': str(tomorrow),
                '0000-0859': self.parse_pharmacy_id(today, 'night'),
                '0900-2159': self.parse_pharmacy_id(tomorrow, 'day'),
                '2200-2359': self.parse_pharmacy_id(tomorrow, 'night'),
            },
        )

    def get_internal_pharmacy_id(self, cofg_pharmacy_id):
        if not self.pharmacies:
            self.pharmacies = list(Pharmacy.objects.all())

        pharmacy = [el for el in self.pharmacies if el.cofg_id == cofg_pharmacy_id][0]
        if pharmacy.place_id not in self.place_ids:
            self.place_ids.append(pharmacy.place_id)

        return pharmacy.place_id

    def parse_pharmacy_id(self, date, guard_time='day'):
        request = self.request_data_from_cofg(date, guard_time)

        if request.status_code == 200:
            cofg_pharmacy_id = int(json.loads(request.text)[0]['id'])
            pharmacy_id = self.get_internal_pharmacy_id(cofg_pharmacy_id)
            return pharmacy_id
        else:
            return None

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

            return post('http://m.cofgipuzkoa.com/ws/cofg_ws.php', data=data)

        except RequestException:
            return { 'status_code': 500 }

