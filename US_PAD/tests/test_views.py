from django.test import TestCase, Client
from django.urls import reverse
import json


class AOI_IntersectViewTests(TestCase):

    AOI_1 = {
        "rings" : [[
            [-119.63833, 37.765101], 
            [-119.63833, 37.965101], 
            [-119.43833, 37.965101], 
            [-119.43833, 37.765101], 
            [-119.63833, 37.765101]
        ]]
    }
        
    AOI_2 = {
        "rings" : [[
            [-124.104631, 41.113181], 
            [-124.104631, 41.313181], 
            [-123.904631, 41.313181], 
            [-123.904631, 41.113181], 
            [-124.104631, 41.113181]
        ]]
    }

    AOI_3 = {
        "rings" : [[
            [-119.869163, 33.896074], 
            [-119.869163, 34.096074], 
            [-119.669163, 34.096074], 
            [-119.669163, 33.896074], 
            [-119.869163, 33.896074]
        ]]
    }

    def setUp(self):
        self.client = Client()

    def test_no_aoi(self):
        response = self.client.post(reverse('padAPI'))
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {"error": "aoi parameter is required"})

    def test_single_aoi(self):
        response = self.client.post(reverse('padAPI'), {"aois": [self.AOI_1]}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        expected_ids = ['expected_id1', 'expected_id2']
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_ids)

    def test_multiple_aoi(self):
        response = self.client.post(reverse('padAPI'), {"aois": [self.AOI_1, self.AOI_2, self.AOI_3]}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        expected_ids = ['expected_id1', 'expected_id2', 'expected_id3']
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_ids)