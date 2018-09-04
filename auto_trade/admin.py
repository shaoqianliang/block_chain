# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from auto_trade import models

# Register your models here.
admin.site.register(models.Account)
# admin.site.register(models.Btc)
admin.site.register(models.Cash)
