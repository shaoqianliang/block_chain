# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from utils.main import *
import matplotlib.pyplot as plt
from django.shortcuts import render, HttpResponse
from io import BytesIO
import threading

# Create your views here.


def back_test(req):
    g = G()
    context = Context(cash, s_date, e_date)
    initialize(context, g)
    global df
    df = run(context, g)
    return render(req, 'test.html', {'cash': cash, 'account': context.positions})


def plot(request):
    plt.plot(df)
    mstream = BytesIO()
    plt.savefig(mstream)
    return HttpResponse(mstream.getvalue())


def auto_trade(req):
    cash = models.Cash.objects.first().cash
    g = G()
    global context
    context = Context(cash, s_date, e_date, status=True)
    obj = models.Account.objects.values('currency', 'cost', 'holding')
    for i in obj:
        current_price = get_now_data(i['currency'])
        context.positions[obj['currency']] = {'cost': obj['cost'], 'holding': obj['holding'], 'order': obj['order'], 'order_cash': obj['order_cash'], 'ratio': obj['cost']/current_price}
    initialize(context, g)
    global df
    df = run(context, g)
    # context.positions['btc'] = {'cost': 40000, 'holding': 2, 'order': 0, 'order_cash': 0}  #填充数据
    # context.positions['eth'] = {'cost': 4000, 'holding': 20, 'order': 10, 'order_cash': 300}
    return render(req, 'my_account.html', {'cash':cash, 'account': context.positions})


def get_price(req):
    import json
    current_list = []
    for i in context.positions:
        if context.positions[i]:
            rel_transact(context, i)
        current_list.append(i)
    currency_price = get_now_data(current_list)
    for k, v in currency_price.items():
        context.positions[k]['ratio'] = v/context.positions[k]['cost']
    models.Account.objects.update(**context.positions)
    return HttpResponse(json.dumps(context.positions))
