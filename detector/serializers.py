from rest_framework import serializers
from .models import Measurement


class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = '__all__'


class PerformAnalysisSerializer(serializers.Serializer):
    device_id = serializers.CharField()
    analysis_name = serializers.CharField()
