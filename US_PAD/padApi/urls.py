from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("aoi-intersect", views.AOI_IntersectView.as_view(), name="aoi-intersect"),
    path("aoi-overlap", views.AOI_IntersectViewOverlap.as_view(), name="aoi-overlap"),
]