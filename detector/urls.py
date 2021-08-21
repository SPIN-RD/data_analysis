from django.urls import path
from .views import MeasurementCreateView

urlpatterns = [
    path('api/measurements/', MeasurementCreateView.as_view()),
]
