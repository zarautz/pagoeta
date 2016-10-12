from datetime import datetime, timedelta
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from .models import Event
from .serializers import TypeField, EventListSerializer
from .views import EventViewSet
from pagoeta.apps.core.functions import get_absolute_uri


class TypeDummyObject(object):
    code = 'code'
    name = 'name'


class TypeFieldTests(TestCase):
    def test_representation(self):
        obj = TypeDummyObject()
        self.assertEqual({'code': obj.code, 'name': obj.name}, TypeField(read_only=True).to_representation(obj))


class EventTests(TestCase):
    fixtures = ['test_data.json']


class EventViewSetListTests(EventTests):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('v1:event-list')

    def test_default_response(self):
        response = self.client.get(self.url)
        from_date = timezone.now()
        to_date = from_date + timedelta(days=EventViewSet.DEFAULT_DAYS_DIFFERENCE)
        visible_events_count = Event.objects.visible().filter(start_date__gte=from_date, end_date__lte=to_date).count()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['meta']['totalCount'], visible_events_count)
        self.assertEqual(len(response.data['data']), visible_events_count)

    def test_parameters_from_invalid(self):
        response = self.client.get(self.url, {'from': '01-01-2013'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_parameters_to_invalid(self):
        response = self.client.get(self.url, {'to': '01-01-2013'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_parameters_to_too_late(self):
        date_format = '%Y-%m-%d'
        from_date = timezone.make_aware(datetime.strptime('2013-01-01', date_format), timezone.get_current_timezone())
        to_date = from_date + timedelta(days=EventViewSet.MAX_DAYS_DIFFERENCE + 10)
        response = self.client.get(self.url, {'from': datetime.strftime(from_date, date_format),
                                              'to': datetime.strftime(to_date, date_format)})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_parameters_to_munoa_exception(self):
        date_format = '%Y-%m-%d'
        to_date = timezone.make_aware(datetime.strptime('2014-02-28', date_format), timezone.get_current_timezone())
        response = self.client.get(self.url, {'to': '2014-02-31'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['meta']['to'], to_date)


class EventViewSetDetailTests(EventTests):
    def setUp(self):
        self.client = APIClient()
        self.event = Event.objects.visible().first()
        self.invisible_event = Event.objects.filter(is_visible=False).first()
        self.timetable_event = Event.objects.get(pk=2)
        self.no_timetable_event = Event.objects.get(pk=3)
        self.serialized_event = EventListSerializer(self.event)
        self.url = reverse('v1:event-detail', args=(self.event.id,))
        self.invisible_url = reverse('v1:event-detail', args=(self.invisible_event.id,))

    def test_default_response(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invisible_event(self):
        response = self.client.get(self.invisible_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_serializer_full_timetable(self):
        self.assertEqual(
            [('12:00', '15:00'), ('18:00', '20:00')],
            self.serialized_event.get_timetable(self.timetable_event)
        )

    def test_serializer_no_timetable(self):
        self.assertEqual((), self.serialized_event.get_timetable(self.no_timetable_event))

    def test_serializer_href(self):
        self.assertEqual(get_absolute_uri(self.url), self.serialized_event.get_href(self.event))
