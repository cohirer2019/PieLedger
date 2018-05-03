# -*- coding:utf-8 -*-
from decimal import Decimal

from sqlalchemy import func
from piecash.core import Split, Account, Transaction

from .base import BaseManager
from .utils import currency_decimal


def _find_with_children(acc):
    yield acc
    for a in acc.children:
        for a in _find_with_children(a):
            yield a


class SplitManager(BaseManager):

    model = Split

    def create(self, transaction, value_str=None, value_int=None, **kwargs):
        kwargs['transaction'] = transaction
        account_guid = kwargs.pop('account')
        kwargs['account'] = self.book.query(Account).get(account_guid)
        if not kwargs['account']:
            raise ValueError('account<%s> not found' % account_guid)
        if transaction.currency != kwargs['account'].commodity:
            raise ValueError('currency must identical')
        if value_str:
            kwargs['value'] = Decimal(value_str)
        elif value_int:
            kwargs['value'] = currency_decimal(
                value_int, transaction.currency
            ) / transaction.currency.fraction
        if kwargs['value'] * transaction.currency.fraction % 1 != 0:
            raise ValueError('invalid value range!')
        Split(**kwargs)

    def find_splits(
            self, account_guid=None, from_dt=None, to_dt=None,
            by_action=None, account_name=None, transref=None,
            page_number=0, result_per_page=None,):
        filters = []
        query = self.book.query(Split)
        count_query = self.session.query(func.count(Split.guid))

        if account_guid:
            acc = account_guid and self.book.query(Account).get(account_guid)
            if not acc:
                raise ValueError('account<%s> not found' % account_guid)
            filters.append(Split.account_guid.in_(
                [a.guid for a in _find_with_children(acc)]))

        if by_action:
            filters.append(Split.action == by_action)
        if from_dt:
            filters.append(
                Split.enter_date >= from_dt.replace(microsecond=0))
        if to_dt:
            filters.append(
                Split.enter_date <= to_dt.replace(microsecond=0))
        if account_name:
            query = query.join(Account)
            count_query = count_query.join(Account)
            filters.append(Account.name == account_name)
        if transref:
            query = query.join(Transaction)
            count_query = count_query.join(Transaction)
            filters.append(Transaction.num == transref)

        query = query.filter(*filters).order_by(
            Split.enter_date.desc())
        result_per_page = result_per_page or 20
        query = query.offset(
            page_number * result_per_page).limit(result_per_page)

        count_query = count_query.filter(*filters)

        return query.all(), count_query.scalar()

    @staticmethod
    def find_inverse(split):
        """Find the most posible split with was tranfering at the inverse
           direction
        """
        sign = split.value > 0
        return (
            s for s in split.transaction.splits
            if (s.value > 0) != sign)
