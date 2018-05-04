# -*- coding:utf-8 -*-
from decimal import Decimal

from sqlalchemy import func
from sqlalchemy.orm import aliased
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
            self, guid=None, account_guid=None, from_dt=None, to_dt=None,
            by_action=None, account_name=None, transref=None,
            inverse_acc_id=None, page_number=0, result_per_page=None):
        filters = []
        query = self.book.query(Split)
        count_query = self.session.query(func.count(Split.guid))

        if guid:
            filters.append(Split.guid == guid)

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

        if transref or inverse_acc_id:
            query = query.join(Transaction)
            count_query = count_query.join(Transaction)

        if transref:
            filters.append(Transaction.num == transref)

        if inverse_acc_id:
            inverse = aliased(Split, name='inverse')
            query = query.join(
                inverse, inverse.transaction_guid == Transaction.guid)
            count_query = count_query.join(
                inverse, inverse.transaction_guid == Transaction.guid)
            filters.extend((
                inverse.account_guid == inverse_acc_id,
                func.sign(inverse._value_num) != func.sign(Split._value_num)))

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
