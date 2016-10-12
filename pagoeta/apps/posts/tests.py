from django.core.urlresolvers import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


class HitzaPostViewSetTests(TestCase):
    def setUp(self):
        self.response = APIClient().get(reverse('v2:hitza-post-list'))

    def test_default_response(self):
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)


class ZuZarautzPostViewSetTests(HitzaPostViewSetTests):
    def setUp(self):
        self.response = APIClient().get(reverse('v1:zuzarautz-post-list'))
