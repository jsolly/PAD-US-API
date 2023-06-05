from .base import SetUp
from django.test import TestCase, Client
from django.urls import reverse
import json
import os
class AOI_IntersectViewTests(TestCase):


    def setUp(self):
        self.client = Client()
        self.base_dir = os.path.dirname(os.path.abspath(__file__))

        with open(os.path.join(self.base_dir, 'AOI_Yosemite.json')) as f:
            self.AOI_Yosemite = json.load(f)

        with open(os.path.join(self.base_dir, 'AOI_Unprotected.json')) as f: # Middle of the Atlantic Ocean
            self.AOI_Unprotected = json.load(f)

    def test_no_aoi(self):
        url = reverse('aoi-intersect')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {"error": "aoi parameter is required"})

    def test_get_intersected_features_for_single_aoi(self):
        url = reverse('aoi-intersect')
        params = {"aoi": json.dumps(self.AOI_Yosemite)}
        response = self.client.get(url, params)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2) # There should be two features that overlap the AOI

    def test_get_no_features_for_unprotected_aoi(self):
        url = reverse('aoi-intersect')
        params = {"aoi": json.dumps(self.AOI_Unprotected)}
        response = self.client.get(url, params)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 0)

    def test_get_overlap_percentage_for_single_aoi(self):
        url = reverse('aoi-overlap')
        intersected_features = []
        base_dir = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(base_dir,'protected_area_1.json')) as f:
            intersected_features.append(json.load(f))

        with open(os.path.join(base_dir,'protected_area_2.json')) as f:
            intersected_features.append(json.load(f))

        params = {"aoi": json.dumps(self.AOI_Yosemite), "intersected_features": json.dumps(intersected_features)}
        response = self.client.get(url, params)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {'Yosemite National Park': {'FED': 100}})
