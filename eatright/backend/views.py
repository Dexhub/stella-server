# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from backend.models import Backend
from backend.serializers import BackendSerializer



# Create your views here.

def index(request):
        return HttpResponse("Hello, world. You're at the polls index.")

@csrf_exempt
def backend_list(request):
    """
    List all code backend, or create a new backend.
    """
    if request.method == 'GET':
        backend = Backend.objects.all()
        serializer = BackendSerializer(backend, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = BackendSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def backend_detail(request, pk):
    """
    Retrieve, update or delete a code backend.
    """
    try:
        backend = Backend.objects.get(pk=pk)
    except Backend.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = BackendSerializer(backend)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = BackendSerializer(backend, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        backend.delete()
        return HttpResponse(status=204)

