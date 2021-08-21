from django.urls import path
from .views import MeasurementCreateView, MeasurementRetrieveView, index, half_life_analysis

urlpatterns = [
    path('api/measurements/', MeasurementCreateView.as_view()),
    path('api/measurements/<str:device_id>/<str:mode>',
         MeasurementRetrieveView.as_view()),
    path('detector/', index, name='index'),
    path('detector/half-life/<str:device_id>',
         half_life_analysis, name='half-life-analysis'),
]
