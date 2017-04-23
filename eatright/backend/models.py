# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles


# Create your models here.

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())


class Backend(models.Model):
    created = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100, blank=True, default='')
    address = models.TextField()
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=3.0)
    distance = models.DecimalField(max_digits=4, decimal_places=1, default=0.0)



class Meta:
    ordering = ('created',)

