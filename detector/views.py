from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpRequest, HttpResponseNotFound
from rest_framework import generics, status, views
from rest_framework.response import Response
from .models import Measurement
from .serializers import MeasurementSerializer


class MeasurementCreateView(generics.CreateAPIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    serializer_class = MeasurementSerializer


class MeasurementRetrieveView(generics.RetrieveAPIView):
    serializer_class = MeasurementSerializer
    queryset = Measurement.objects.all()

    def get(self, request, device_id, mode):
        qs = Measurement.objects.filter(
            device_id=device_id, mode=mode).order_by('-created_at').first()
        if not qs:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

        return Response(MeasurementSerializer(qs).data)


def index(request):
    context = {}
    return render(request, "detector/index.html", context)


def half_life_analysis(request, device_id):
    latest_measurement = Measurement.objects.filter(
        device_id=device_id, mode='Linear').order_by('-created_at').first()

    if not latest_measurement:
        return HttpResponseNotFound()

    json_data = latest_measurement.measurement_data

    context = {
        'analysis': {},
        'device_id': device_id,
        'json_data': json_data
    }

    return render(request, 'detector/half_life_analysis.html', context)
