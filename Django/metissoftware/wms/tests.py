import unittest
from django.test import Client, TestCase
from wms.models import Client as c
from wms.models import FA
import wms.views

# Create your tests here.


class TestResponse(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.client.login(username='root@metis.com', password='pass')

    def test_client_details(self):
        response = self.client.get('/client_details/client?=JG123456A')
        self.assertEqual(response.status_code, 302)

    def test_client_list(self):
        response = self.client.get('/clients/')
        self.assertEqual(response.status_code, 302)


class ClientTestCase(TestCase):
    def setUp(self):
        c.objects.create(first_name="test", surname="testsurname",
                         dob="1989-06-23", ni_number="AB521426C",
                         email="testcase@metis.com",
                         home_phone="07817777777", mob_phone="01365233234",
                         cash="23.45"
                         )

    def testGetClient(self):
        c.objects.get(ni_number="AB521426C")


class FATestCase(TestCase):
    def setUp(self):
        FA.objects.create(first_name="testfa", surname="testsurnamefa",
                          dob="1989-06-23", ni_number="AB521426C",
                          email="testcasefa@metis.com",
                          )

    def testGetFA(self):
        FA.objects.get(email="testcasefa@metis.com")
