from django.http import JsonResponse
from django.views import View
import json
import requests
from shapely.geometry import Polygon, MultiPolygon
# Create your views here.
from django.http import HttpResponse


def index(request):
    return HttpResponse("Welcome to the Protected Area Database API! Please refer to the Readme for usage instructions.")


class AOI_IntersectView(View):
    def get(self, request, *args, **kwargs):
        # Retrieve AOI from request parameters
        aoi = request.GET.get('aoi')
        if not aoi:
            return JsonResponse({"error": "aoi parameter is required"}, status=400)

        # Parse the AOI from JSON
        try:
            aoi = json.loads(aoi)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid AOI JSON"}, status=400)

        # Construct the ArcGIS API URL
        url = "https://services.arcgis.com/v01gqwM5QqNysAAi/arcgis/rest/services/Protection_Status_by_GAP_Status_Code/FeatureServer/0/query"

        # Define the parameters for the request
        spatial_reference = json.dumps(aoi["spatialReference"]["wkid"])
        data = {
            "f": "json",
            "where": "1=1",
            "outFields": "*",
            "geometryType": "esriGeometryPolygon",
            "inSR": spatial_reference,
            "outSR": spatial_reference,
            "geometry": json.dumps(aoi["features"][0]["geometry"]),
            "spatialRel": "esriSpatialRelIntersects",
        }


        # Send the request to the ArcGIS API
        response = requests.post(url, data=data)

        # Parse the response
        resp = response.json()
        features = resp.get("features", [])

        return JsonResponse(features, safe=False)  # wrap list in JsonResponse



class AOI_IntersectViewOverlap(View):
    def get(self, request, *args, **kwargs):
        # Retrieve AOI and intersected_features from request parameters
        aoi_json = request.GET.get('aoi')
        intersected_features_json = request.GET.get('intersected_features')
        if not aoi_json or not intersected_features_json:
            return JsonResponse({"error": "Both aoi and intersected_features parameters are required"}, status=400)

        # Parse the AOI and intersected_features from JSON
        try:
            aoi = json.loads(aoi_json)
            intersected_features = json.loads(intersected_features_json)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        # Create a MultiPolygon from the AOI
        aoi_geometry = aoi["features"][0]["geometry"]["rings"]
        aoi_multipolygon = MultiPolygon([Polygon(ring) for ring in aoi_geometry])
        aoi_area = aoi_multipolygon.area

        # Initialize the result dictionary
        aoi_name = aoi["features"][0]["attributes"]["Name"]
        result = {aoi_name: {}}

        # Calculate the area of the intersected features and the percentage of the total AOI
        for feature in intersected_features:
            feature_geometry = feature["geometry"]["rings"]
            feature_multipolygon = MultiPolygon([Polygon(ring) for ring in feature_geometry])
            feature_area = feature_multipolygon.intersection(aoi_multipolygon).area

            # Use the "Mang_Type" attribute as key
            mang_type = feature["attributes"]["Mang_Type"]

            # Sum the percentages if the "Mang_Type" is already in the dictionary
            if mang_type in result[aoi_name]:
                result[aoi_name][mang_type] += feature_area / aoi_area * 100
            else:
                result[aoi_name][mang_type] = feature_area / aoi_area * 100

        # Round the percentages to the nearest whole number
        for mang_type in result[aoi_name]:
            result[aoi_name][mang_type] = round(result[aoi_name][mang_type])

        return JsonResponse(result)
