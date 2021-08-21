from django.urls import path
from .views import MeasurementCreateView, index, half_life_analysis

urlpatterns = [
    path('api/measurements/', MeasurementCreateView.as_view()),
    path('detector/', index, name='index'),
    path('detector/half-life/<str:device_id>',
         half_life_analysis, name='half-life-analysis')
]
