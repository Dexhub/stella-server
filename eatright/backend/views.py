# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from backend.models import ItemInfo, Loc2RestMenu, RestaurantInfo, ItemRating
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
    response = {}

    query_result = gmaps.places_nearby( location = location, keyword='Restaurants', type='restaurant',rank_by='distance',open_now=True)

    restaurants = []
    for result in query_result["results"]:
        restaurant = {}
        restaurant["id"] = result["id"]
        restaurant["name"] = result["name"]
        restaurant["placeId"] = result["place_id"]
        restaurant["rating"] = result["rating"]
        restaurant["address"] = result["vicinity"]
        restaurant["lat"] = result["geometry"]["location"]["lat"]
        restaurant["lng"] = result["geometry"]["location"]["lng"]
        loc = (restaurant["lat"], restaurant["lng"])
        restaurant["distance"] = round(vincenty(location, loc).miles, 1)
        restaurants.append(restaurant)

    sorted_restaurants = sorted(restaurants, key=lambda k: k['rating'], reverse=True)
    response["status"] = 200
    response["message"] = "Success"
    response["result"]={}

    response["result"]["restaurants"] = sorted_restaurants
    return JsonResponse(response, status=200,safe=False)



@csrf_exempt
def get_menu_info(request):
    """ 
    Get Menu info.
    """
    response = {}
    response["result"] = {}

    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    lat = body['lat']
    lng = body['lng']
    try:
        row_id = Loc2RestMenu.objects.get(lat = lat, lng = lng)
        print "Restaurant id: %s " % (row_id.restid)
        print "Get all Menu based on restaurant id and generate a json object"

        # Get all menu info
        items = []

        for i in ItemInfo.objects.filter(restid = row_id.restid):
            item = {}
            item["itemId"]= i.itemid
            item["itemName"] = i.itemname
            item["price"] = i.price
            item["rating"] = i.rating
            item["desc"] = i.description
            item["type"] = i.type
            items.append(item)

        #Print "Found %s menu items for restaurant id %s" % (len(menu_items), row_id.restid)

        # Get the restaurant id matching lat and lng
        sorted_items = sorted(items, key=lambda k: k['itemId'], reverse=False)

        response["status"] = 200
        response["message"] = "Success"

        response["result"]["items"] = sorted_items
        response["result"]["restId"] = row_id.restid

        return JsonResponse(response, status=200, safe=False)

    except Loc2RestMenu.DoesNotExist:

        response["status"] = 404
        response["message"] = "Fail"

        googleId = body["id"]

        try:
            row_id = RestaurantInfo.objects.get(sourceid=googleId)
            print "status=\"error message\" \"Looks like a popular restaurant's menu is missing\" googleId="+googleId
            response["errMessage"] = "Missing menu for a new restaurant. Restaurant is already marked missing"

        except RestaurantInfo.DoesNotExist:
            print "status=\"error\" message=\"Google result restaurant missing menu in db\" googleId=" + googleId
            name = body["name"]
            address = body["address"]
            placeId = body["placeId"]
            rating = body["rating"]
            restaurant_object = RestaurantInfo(name=name, address=address, rating=rating, source="Google", placeid=placeId, sourceid=googleId)
            #restaurant_object.save()
            response["errMessage"] = "Missing menu for a new restaurant. Restaurant added in DB"

        return JsonResponse(response, status=404,safe=False)

@csrf_exempt
def post_rating(request):
    """
    List all nearby restaurants.
    """
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        response = {}
        response["result"] = {}

        rest_id = body['restId']
        user_id = body['userId']
        item_id = body['itemId']
        rating = body['rating']
        comment = body['comment']

        rating_object = ItemRating(rest_id=rest_id,
                           user_id = user_id,
                           item_id = item_id,
                           rating = rating, comment=comment )
        rating_object.save()
        response["status"] = 200
        response["message"] = "Success"


        response["result"]['restId'] = rest_id
        response["result"]['userId'] = user_id
        response["result"]['itemId'] = item_id
        response["result"]['rating'] = rating
        response["result"]['comment'] = comment

        return JsonResponse(response, status=200,safe=False)
