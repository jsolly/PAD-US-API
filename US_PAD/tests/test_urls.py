from .base import SetUp
from django.urls import reverse, resolve
from padApi import views
import json

class TestUrls(SetUp):

    def test_padApi_base_url_is_resolved(self):
        url = reverse('index')
        self.assertEqual(resolve(url).func, views.index)

    def test_aoi_intersect_url_is_resolved(self):
        url = reverse('aoi-intersect')
        
        # Create a mock AOI as a dictionary
        aoi_mock = {
            "spatialReference": {"wkid": 102100},
            "features": [{
                "geometry": {
                    "rings": [
                        [
                            [3837532.340042665, 4938088.828634524],
                            [3837532.340042665, 5075580.730771197],
                            [3975024.242179338, 5075580.730771197],
                            [3975024.242179338, 4938088.828634524],
                            [3837532.340042665, 4938088.828634524]
                        ]
                    ]
                }
            }]
        }

        aoi_json = json.dumps({'aoi': aoi_mock})

        # Send a POST request with the AOI as JSON in the request body
        response = self.client.post(url, data=aoi_json, content_type='application/json')
        self.assertEqual(response.status_code, 200)
