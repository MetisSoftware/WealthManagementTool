from django.test import TestCase
from wms.models import Client

class ClientTestCase(TestCase):
    def setUp(self):
        Client.objects.create(first_name="test", surname="test2", email="test@unitest.com")
