# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-07-14 08:06
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auto_trade', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='account',
        ),
        migrations.DeleteModel(
            name='Btc',
        ),
    ]
