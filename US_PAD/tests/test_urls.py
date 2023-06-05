from .base import SetUp
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from padApi import views

class TestUrls(SimpleTestCase):

    def test_padApi_base_url_is_resolved(self):
        url = reverse('index')
        self.assertEqual(resolve(url).func, views.index)



    def test_aoi_intersect_url_is_resolved(self):
        url = reverse('aoi-intersect')
        
        # Add the necessary 'aoi' data to the GET request
        data = {
            'aoi': ['value1', 'value2'],  # Replace with actual AOI values
        }
        
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, 200)
