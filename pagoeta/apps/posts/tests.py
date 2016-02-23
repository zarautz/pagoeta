from django.core.urlresolvers import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


class HitzaPostViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('v1:hitza-post-list')

    def test_default_response(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ZuZarautzPostViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('v1:zuzarautz-post-list')

    def test_default_response(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
