from datetime import datetime, timedelta
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from .models import Event
from .views import EventViewSet


class EventViewSetListTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('v1:event-list')

    def test_default_response(self):
        response = self.client.get(self.url)
        from_date = timezone.now()
        to_date = from_date + timedelta(days=EventViewSet.DEFAULT_DAYS_DIFFERENCE)
        visible_events_count = Event.objects.visible().filter(start_at__gte=from_date, end_at__lte=to_date).count()
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
        from_date = timezone.make_aware(datetime.strptime('2013-01-01', date_format))
        to_date = from_date + timedelta(days=EventViewSet.MAX_DAYS_DIFFERENCE + 10)
        response = self.client.get(self.url, {'from': datetime.strftime(from_date, date_format),
                                              'to': datetime.strftime(to_date, date_format)})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class EventViewSetDetailTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.event = Event.objects.visible().first()
        self.invisible_event = Event.objects.filter(is_visible=False).first()
        self.url = reverse('v1:event-detail', args=(self.event.id,))
        self.invisible_url = reverse('v1:event-detail', args=(self.invisible_event.id,))

    def test_default_response(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invisible_event(self):
        response = self.client.get(self.invisible_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
