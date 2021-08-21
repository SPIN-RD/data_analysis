from django.contrib import admin
from .models import Measurement


class MeasurementAdmin(admin.ModelAdmin):
    list_display = ('device_id', 'mode', 'created_at')
    list_filter = ('mode', 'device_id')


admin.site.register(Measurement, MeasurementAdmin)
