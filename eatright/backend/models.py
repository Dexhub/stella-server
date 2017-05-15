# This is an auto-generated Django model module.
from __future__ import unicode_literals

from django.db import models


class ItemInfo(models.Model):
    itemid = models.AutoField(primary_key=True)
    restid = models.ForeignKey('RestaurantInfo', models.DO_NOTHING, db_column='restid')
    itemname = models.TextField()
    ingredients = models.TextField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)
    ratinglist = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    vegan = models.IntegerField(blank=True, null=True)
    vegetarian = models.IntegerField(blank=True, null=True)
    glutenfree = models.IntegerField(blank=True, null=True)
    spicylevel = models.FloatField(blank=True, null=True)
    calories = models.IntegerField(blank=True, null=True)
    type = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'item_info'


class Loc2RestMenu(models.Model):
    tableid = models.AutoField(primary_key=True)
    lat = models.FloatField()
    lng = models.FloatField()
    locindex = models.TextField()
    restid = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'loc_2_rest_menu'


class RestaurantInfo(models.Model):
    restid = models.AutoField(primary_key=True)
    name = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    rating = models.DecimalField(max_digits=4, decimal_places=4, blank=True, null=True)
    zipcode = models.DecimalField(max_digits=8, decimal_places=0, blank=True, null=True)
    ratinglist = models.TextField(blank=True, null=True)
    cusine = models.TextField(blank=True, null=True)
    tags = models.TextField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'restaurant_info'
