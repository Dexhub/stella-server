# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from backend.models import Backend
from backend.serializers import BackendSerializer
import logging

import googlemaps
from datetime import datetime
import json
from geopy.distance import vincenty

# Create your views here.
gmaps = googlemaps.Client(key='AIzaSyBCvRzeb_-A2AKvKM0A5MqXkuKclf08gM4')
logger = logging.getLogger(__name__)


@csrf_exempt
def get_restaurant_list(request):
    """ 
    List all nearby restaurants.
    """
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    location = (body['lat'], body['lon'])

    query_result = gmaps.places_nearby( location = location, keyword='Restaurants', type='restaurant',rank_by='distance',open_now=True)

    response = []
    for result in query_result["results"]:
        resp = {}
        resp["id"] = result["id"]
        resp["name"] = result["name"]
        resp["place_id"] = result["place_id"]
        resp["rating"] = result["rating"]
        resp["address"] = result["vicinity"]
        resp["lat"] = result["geometry"]["location"]["lat"]
        resp["lng"] = result["geometry"]["location"]["lng"]
        rest_loc = (resp["lat"], resp["lng"])
        resp["distance"] = (vincenty(location, rest_loc).miles)
        response.append(resp)

    print response
    new_list = sorted(response, key=lambda k: k['rating'], reverse=True)
    return JsonResponse(new_list, status=200,safe=False)




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

