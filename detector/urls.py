from django.urls import path
from .views import MeasurementCreateView, PerformAnalysisView, ListAnalysesView
from . import views

urlpatterns = [
    path('api/measurements/', MeasurementCreateView.as_view()),
    path('api/measurements/analyze/', PerformAnalysisView.as_view()),
    path('api/analyses/', ListAnalysesView.as_view()),
    path('', views.index, name='index'),
    path('<int:device_id>/', views.detail, name='detail')
]