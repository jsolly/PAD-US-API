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

        # Convert the AOI to a JSON string
        aoi_json = json.dumps(aoi_mock)

        # Add the necessary 'aoi' data to the GET request
        data = {
            'aoi': aoi_json
        }
        
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, 200)