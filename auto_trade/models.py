# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


# class Btc(models.Model):
#     datetime = models.DateField(primary_key=True)
#     currency = models.CharField(max_length=10)
#     high = models.DecimalField(max_digits=10, decimal_places=4)
#     low = models.DecimalField(max_digits=10, decimal_places=4)
#     close = models.DecimalField(max_digits=10, decimal_places=4)
#     volume = models.DecimalField(max_digits=10, decimal_places=4)
#     average = models.DecimalField(max_digits=10, decimal_places=4)
#     turnover = models.DecimalField(max_digits=12, decimal_places=4)
#
#     def __str__(self):
#         return self.currency


class Account(models.Model):
    currency = models.CharField(max_length=10)
    cost = models.DecimalField(max_digits=10, decimal_places=4)
    # market_value = models.DecimalField(max_digits=10, decimal_places=4)
    holding = models.DecimalField(max_digits=10, decimal_places=4)
    order = models.DecimalField(max_digits=10, decimal_places=4)
    order_cash = models.DecimalField(max_digits=10, decimal_places=4)
    # profit_loss_ratio = models.DecimalField(max_digits=5, decimal_places=2)
    # assets = models.DecimalField(max_digits=10, decimal_places=4)

    def __str__(self):
        return str(self.currency)


class Cash(models.Model):
    cash = models.CharField(max_length=10)