# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-09-02 10:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auto_trade', '0005_auto_20180714_1818'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cash',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cash', models.CharField(max_length=10)),
            ],
        ),
        migrations.RemoveField(
            model_name='account',
            name='assets',
        ),
        migrations.RemoveField(
            model_name='account',
            name='market_value',
        ),
        migrations.RemoveField(
            model_name='account',
            name='profit_loss_ratio',
        ),
    ]
