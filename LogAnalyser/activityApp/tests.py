from django.test import TestCase
from django.test.client import Client
from activityApp.models import *
import log_analyse, json

class CountHourlyTest(TestCase):
    def setUp(self):
        log_analyse.parse()
        print Activity.objects.count()

    def testSucceess(self):
        c = Client()
        response = c.get('/activity/count/hourly/?date=2012-09-29')
        return_dict = json.loads(response.content)
        self.assertTrue(return_dict.has_key('status'))
        self.assertEqual(return_dict['status']['code'], 'OK')
        self.assertTrue(return_dict.has_key('hour_count'))
        self.assertEqual(return_dict['hour_count']['23'], 4)
