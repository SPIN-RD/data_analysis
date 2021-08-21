from django.shortcuts import render
from django.http import HttpResponse
import datetime

def index(request):
    return HttpResponse("Hello, world. You're at the detector index.")

def detail(request, device_id):
    return HttpResponse(f"Detailed overview of device id {device_id}")
