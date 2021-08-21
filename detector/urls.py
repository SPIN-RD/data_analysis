from django.urls import path
from .views import MeasurementCreateView, PerformAnalysisView, ListAnalysesView

urlpatterns = [
    path('api/measurements/', MeasurementCreateView.as_view()),
    path('api/measurements/analyze/', PerformAnalysisView.as_view()),
    path('api/analyses/', ListAnalysesView.as_view())
]
