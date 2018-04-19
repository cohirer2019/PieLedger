# -*- coding:utf-8 -*-
from decimal import Decimal
from piecash.core import Split, Account

from .base import BaseManager
from .utils import currency_decimal


class SplitManager(BaseManager):

    model = Split

    def create(self, transaction, value_str=None, value_int=None, **kwargs):
        kwargs['transaction'] = transaction
        account_guid = kwargs.pop('account')
        kwargs['account'] = self.book.query(Account).get(account_guid)
        if not kwargs['account']:
            raise ValueError('account<%s> not found' % account_guid)
        if value_str:
            kwargs['value'] = Decimal(value_str)
        elif value_int:
            kwargs['value'] = currency_decimal(
                value_int, transaction.currency) / transaction.currency.fraction
        if kwargs['value'] * transaction.currency.fraction % 1 != 0:
            raise ValueError('invalid value range!')
        Split(**kwargs)
