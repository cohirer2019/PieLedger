# -*- coding:utf-8 -*-
from decimal import Decimal


def currency_decimal(value, currency):
    q = Decimal(1) / currency.fraction
    return Decimal(value).quantize(q)
