# -*- coding:utf-8 -*-
from decimal import Decimal

import pytz


def currency_decimal(value, currency):
    q = Decimal(1) / currency.fraction
    return Decimal(value).quantize(q)


def normalize_dt(value):
    if not value.tzinfo:
        value = pytz.utc.localize(value)
    return value.replace(microsecond=0)
