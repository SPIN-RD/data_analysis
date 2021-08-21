from django.shortcuts import render
from rest_framework import generics
from .models import Measurement
from .serializers import MeasurementSerializer


class MeasurementCreateView(generics.CreateAPIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    # queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer
