from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
import requests
import json
# Create your views here.
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")




class AOI_IntersectView(View):
    def get(self, request, *args, **kwargs):
        # Get area of interest from request parameters
        aoi_list = request.GET.getlist('aoi')
        if not aoi_list:
            return JsonResponse({"error": "aoi parameter is required"}, status=400)

        # Construct the ArcGIS API URL
        url = "https://services.arcgis.com/v01gqwM5QqNysAAi/arcgis/rest/services/Protection_Status_by_GAP_Status_Code/FeatureServer/0/query"

        global_ids = []

        for aoi in aoi_list:
            # Define the parameters for the request
            params = {
                'f': 'json',
                'where': '1=1',
                'outFields': 'GlobalID',
                'geometryType': 'esriGeometryEnvelope',
                'geometry': aoi,
                'spatialRel': 'esriSpatialRelIntersects',
            }

            # Send the request to the ArcGIS API
            response = requests.get(url, params=params)

            # Parse the response
            data = response.json()
            features = data.get('features', [])

            # Extract the GlobalID and add them to the list
            global_ids.extend([feature['attributes']['GlobalID'] for feature in features if 'attributes' in feature and 'GlobalID' in feature['attributes']])

        return JsonResponse(global_ids, safe=False)