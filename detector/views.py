from django.shortcuts import render
from rest_framework import generics, status, views
from rest_framework.response import Response
from .models import Measurement
from .serializers import MeasurementSerializer, PerformAnalysisSerializer
from .analyses import find_analysis, analyses


class MeasurementCreateView(generics.CreateAPIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    serializer_class = MeasurementSerializer


class ListAnalysesView(views.APIView):
    def get(self, request):
        names = []
        for analysis_wrapper in analyses:
            names.append(analysis_wrapper.name)
        return Response(names)


class PerformAnalysisView(generics.GenericAPIView):
    serializer_class = PerformAnalysisSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({'code': 'input_error', 'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        device_id = data['device_id']
        analysis_name = data['analysis_name']

        result = self.do_analysis(analysis_name, device_id)
        if not result:
            return Response({'error': 'Analysis not found or data is insufficient'}, status=status.HTTP_404_NOT_FOUND)

        return Response(data=result)

    def do_analysis(self, name, device_id):
        analysis = find_analysis(name)
        if not analysis:
            return None

        analysis_cls, mode = analysis
        latest_compatible_measurement = Measurement.objects.filter(
            mode=mode, device_id=device_id).order_by('-created_at').first()

        if not latest_compatible_measurement:
            return None

        data = latest_compatible_measurement.measurement_data
        if not data:
            return None

        return analysis_cls().analyze(data)
