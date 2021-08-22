from django.urls import path

from .views import (
    MeasurementCreateView,
    MeasurementRetrieveView,
    energy_spectrum_analysis,
    half_life_analysis,
    index,
)

urlpatterns = [
    path("api/measurements/", MeasurementCreateView.as_view()),
    path(
        "api/measurements/<str:device_id>/<str:mode>", MeasurementRetrieveView.as_view()
    ),
    path("", index, name="index"),
    path(
        "detector/half-life/<str:device_id>",
        half_life_analysis,
        name="half-life-analysis",
    ),
    path(
        "detector/energy-spectrum/<str:device_id>",
        energy_spectrum_analysis,
        name="energy-spectrum-analysis",
    ),
]
