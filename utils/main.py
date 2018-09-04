# -*- coding: utf-8 -*-
import pandas as pd
from auto_trade import models
import datetime
import requests
account = models.Account.objects.values()
trade_cal = pd.read_csv('trade_cal.csv')#暂时没数据,交易时间
request = requests.session()

class G:
    pass


class Context:
    def __init__(self, cash, start_date, end_date, status=False):
        self.cash = cash
        self.start_date = start_date
        self.end_date = end_date
        self.positions = {}
        self.status = status
        self.date_range = trade_cal[(trade_cal.calendarDate >= start_date)
                                    & (trade_cal.calendarDate <= end_date)]['calendarDate'].values


cash = 100000.0
s_date = '2014-01-01'
e_date = '2017-01-01'



def attribute_daterange_history(currency, start_date, end_date,
                      fields=('open', 'low', 'volume', 'turnover')):
    """当天以前历史数据"""
    f = open(currency + '.csv', 'r')
    df = pd.read_csv(f, index_col='date', parse_dates=['date']).loc[start_date:end_date, :]
    return df[list(fields)].sort_index()


def _order(context,today_data, currency, amount):
    """提交订单"""
    if today_data.empty:
        print("停止交易")
        return False

    if currency not in context.positions: #{'btc':{'holding':2 ,'cost':48000}}
        context.positions[currency]['holding'] = 0

    if context.cash - amount * today_data * 1.0003 < 0:
        amount = int(context.cash / today_data / 1.0003)
        print("现金不足，已调整为%d" % amount)

    if context.positions[currency]['holding'] + amount < 0:
        amount = - context.positions[currency]
        print("卖出数量必须不超过持仓数，已调整为%d" % amount)

    action = "买入" if amount > 0 else "卖出"
    if context.status == True:
        real_trade(amount, today_data)
    print "%s: %s%s货币%d枚，价格%.2f" % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M'), action, currency, amount, today_data)
    if amount < 0:
        new_amount = context.positions[currency]['holding'] + amount
        context.positions[currency]['holding'] = new_amount

    if amount > 0:
        context.cash -= amount * today_data * 1.0003
        context.positions[currency]['holding'] += amount
    else:
        context.cash -= amount * today_data * 0.9987
        context.positions[currency]['cost'] = today_data
    if context.positions[currency]['holding'] == 0:
        del context.positions[currency]


def real_trade(context, currency, amount, today_data):
    """登录，提交订单"""
    context.positions[currency]['order'] = amount
    if amount > 0:
        context.positions[context]['order-cash'] = amount*today_data
        context.cash -= amount*today_data
    else:
        context.positions['holding'] += amount
        rel_transact(currency)
    pass


def rel_transact(context, currency):
    """实际成交"""
    rel = request.get(url='')
    amount = 20 #成交量
    today_data = 10 #成交价
    context.positions[currency]['holding'] += amount
    context.cash -= amount * today_data
    if amount > 0:
        cost = context.positions[currency]['holding']*context.positions[currency]['cost']
        context.positions[currency]['order'] -= amount
        context.positions[currency]['cost'] = (cost+amount*today_data)/context.positions[currency]['holding']
    else:
        context.positions['holding'] += amount


def get_now_data(currency):
    """当前价格"""
    from bs4 import BeautifulSoup
    result = requests.get(url='ip地址')
    rel = BeautifulSoup(result, 'parse.html')
    if datetime.datetime.strftime('%H-%M-%S') == '24-00-00':
        """更新历史数据"""
        pass
    return '成交价%s' %currency  #字典格式返回


def order(context, currency, cash):
    today_data = get_now_data(currency)
    amount = cash/today_data
    return _order(context, today_data, currency, amount,)


def run(context, g):
    init_value = cash
    plt_df = pd.DataFrame(index=pd.to_datetime(context.date_range), columns=['value'])
    handle_data(context, g)
    value = context.cash
    for stock in context.positions:
        today_data = get_now_data(stock)
        prize = today_data
        context.positions[stock]['ratio'] = context.positions[stock]/today_data
        value += prize * context.positions[stock]['holding'] #币市值
    plt_df.loc[datetime.datetime.now().strftime('%Y-%m-%d'), 'value'] = value
    plt_df['ratio']  = (plt_df['value'] - init_value) / init_value
    return plt_df.loc[datetime.datetime.now().strftime('%Y-%m-%d'):, ['value', 'ratio']]


def initialize(context, g):
    """自选，均线选择"""
    g.currency = ['BTC'] #自选币种
    g.p1 = 5
    g.p2 = 10


def handle_data(context, g):
    n = len(g.currency)
    for stock in g.currency:
        hist = attribute_daterange_history(stock, (datetime.datetime.now()-datetime.timedelta(days=g.p2)).strftime('%Y-%m-%d'), datetime.datetime.now())
        ma1 = hist['open'][-g.p1:].mean()
        ma2 = hist['open'].mean()
        if ma1 > ma2 and stock not in context.positions:
            order(context, stock, context.cash / n)
        elif ma1 < ma2 and stock in context.positions:
            order(context, stock, 0)



