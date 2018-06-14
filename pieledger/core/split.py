# -*- coding:utf-8 -*-
from __future__ import division

from sqlalchemy import func
from sqlalchemy.orm import aliased
from piecash.core import Split, Account, Transaction

from .base import BaseManager
from .utils import currency_decimal, normalize_dt


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
        value = float(value_str) if value_str else \
            value_int / transaction.currency.fraction
        if value * transaction.currency.fraction % 1 != 0:
            raise ValueError('invalid value range!')
        kwargs['value'] = currency_decimal(value, transaction.currency)
        Split(**kwargs)

    def find_splits(  # noqa
            self, guid=None, account_guid=None, from_dt=None, to_dt=None,
            by_action=None, account_name=None, transref=None,
            inverse_acc_id=None, page_number=0, result_per_page=None):

        filters = []
        query = self.book.query(Split)

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
            filters.append(Split.enter_date >= normalize_dt(from_dt))
        if to_dt:
            filters.append(Split.enter_date <= normalize_dt(to_dt))

        if account_name:
            query = query.outerjoin(Account)
            filters.append(Account.name == account_name)

        if transref or inverse_acc_id:
            query = query.outerjoin(Transaction)

        if transref:
            filters.append(Transaction.num == transref)

        if inverse_acc_id:
            inverse = aliased(Split, name='inverse')
            query = query.outerjoin(
                inverse, inverse.transaction_guid == Transaction.guid
            ).group_by(Split.guid)
            filters.extend((
                func.sign(inverse._value_num) != func.sign(Split._value_num),
                inverse.account_guid == inverse_acc_id))

        query = query.filter(*filters)
        count = self.get_count(query)

        # Pre-join for results
        query = self.eager_load(query, Transaction, Split.transaction)
        query = self.eager_load(query, Account, Split.account)
        query = self.eager_load(
            query, aliased(Account, name='parent_acc'), Split.account,
            Account.parent)

        # Paging
        result_per_page = result_per_page or 20
        query = query.order_by(
            Split.enter_date.desc()).offset(
                page_number * result_per_page).limit(result_per_page)

        return query.all(), count

    def find_inverses(self, splits):
        split_map = {s.guid: s for s in splits}
        inverse = aliased(Split, name='inverse')

        query = self.book.query(Split).join(Transaction).join(
            inverse, Transaction.guid == inverse.transaction_guid
        ).filter(
            func.sign(inverse._value_num) != func.sign(Split._value_num),
            Split.guid.in_(split_map.keys())
        )

        # Pre-join for results
        query = self.eager_load(query, Transaction, Split.transaction)
        query = self.eager_load(
            query, inverse, Split.transaction, Transaction.splits)
        query = self.eager_load(
            query, Account, Split.transaction, Transaction.splits,
            inverse.account)
        query = self.eager_load(
            query, aliased(Account, name='parent_acc'), Split.transaction,
            Transaction.splits, inverse.account, Account.parent)

        for s in query:
            split_map[s.guid].inverses = s.transaction.splits
