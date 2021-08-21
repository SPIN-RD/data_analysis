from django.urls import path
from .views import MeasurementCreateView, PerformAnalysisView, ListAnalysesView, index, detail

urlpatterns = [
    path('api/measurements/', MeasurementCreateView.as_view()),
    path('api/measurements/analyze/', PerformAnalysisView.as_view()),
    path('api/analyses/', ListAnalysesView.as_view()),
    path('detector/', index, name='index'),
    path('detector/<int:device_id>/<str:analysis_name>', detail, name='detail')
]