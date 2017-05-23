# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from backend.models import ItemInfo, Loc2RestMenu, RestaurantInfo
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
    location = (body['lat'], body['lng'])

    query_result = gmaps.places_nearby( location = location, keyword='Restaurants', type='restaurant',rank_by='distance',open_now=True)

    response = []
    for result in query_result["results"]:
        resp = {}
        resp["id"] = result["id"]
        resp["name"] = result["name"]
        resp["placeId"] = result["place_id"]
        resp["rating"] = result["rating"]
        resp["address"] = result["vicinity"]
        resp["lat"] = result["geometry"]["location"]["lat"]
        resp["lng"] = result["geometry"]["location"]["lng"]
        loc = (resp["lat"], resp["lng"])
        resp["distance"] = round(vincenty(location, loc).miles, 1)
        response.append(resp)

    print response
    new_list = sorted(response, key=lambda k: k['rating'], reverse=True)
    return JsonResponse(new_list, status=200,safe=False)


@csrf_exempt
def get_menu_info(request):
    """ 
    Get Menu info.
    """
    response = []
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    lat = body['lat']
    lng = body['lng']
    row_id = Loc2RestMenu.objects.get(lat = lat, lng = lng)

    print "Restaurant id: %s " % (row_id.restid)
    print "Get all Menu based on restaurant id and generate a json object"

    # Get all menu info
    resp = {}
    resp["restId"] = row_id.restid

    for item in ItemInfo.objects.filter(restid = row_id.restid):
        resp = {}
        resp["itemId"]= item.itemid
        resp["itemName"] = item.itemname
        resp["price"] = item.price
        resp["rating"] = item.rating
        resp["desc"] = item.description
        resp["type"] = item.type
        response.append(resp)

    # Print "Found %s menu items for restaurant id %s" % (len(menu_items), row_id.restid)

    # Get the restaurant id matching lat and lng 

    # Print response

    new_list = sorted(response, key=lambda k: k['itemId'], reverse=False)
    return JsonResponse(new_list, status=200,safe=False)
