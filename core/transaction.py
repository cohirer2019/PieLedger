# -*- coding:utf-8 -*-
from sqlalchemy import func, distinct
from piecash.core import Transaction, Split, Account

from .base import BaseManager


class TransactionManager(BaseManager):

    def __init__(self, book, *args, **kwargs):
        super(TransactionManager, self).__init__(book)
        self.session = self.book.session

    def map(self, **kwargs):
        splits = kwargs.pop('splits')
        kwargs['splits'] = []
        for split in splits:
            account_guid = split.pop('account')
            split['account'] = self.book.query(Account).get(account_guid)
            if not split['account']:
                raise ValueError('account not exist')

            s_guid = split.pop('guid', None)
            if s_guid:
                split['quantity'] = split['value']
                _split = self.book.query(Split).get(s_guid)
                if not _split:
                    raise ValueError('split<%s> not found' % s_guid)
                for k, v in split.items():
                    setattr(_split, k, v)
                kwargs['splits'].append(_split)
            else:
                kwargs['splits'].append(Split(**split))
        return kwargs

    def find_by_guid(self, guid):
        return self.book.query(Transaction).get(guid)

    def find_transaction(
            self, guids, account_id, page_number, result_per_page):

        filters = [
            Transaction.guid.in_(guids),
            Split.account_guid == account_id
        ]

        transactions = self.session.query(Transaction).join(
            Split, Split.transaction_guid == Transaction.guid
        ).group_by(Transaction.guid).filter(
            *filters
        ).order_by(Transaction.enter_date)
        transactions_page = transactions.offset(
            page_number * result_per_page).limit(result_per_page).all()

        count_query = self.session.query(
            func.count(distinct(Split.transaction_guid))).filter(*filters)

        return transactions_page, count_query.scalar()

    def create_transaction(self, **kwargs):
        kwargs['currency'] = self.book.default_currency
        kwargs = self.map(**kwargs)
        return Transaction(**kwargs)

    def alter_transaction(self, **kwargs):
        transaction = self.find_by_guid(kwargs.get('guid'))
        if not transaction:
            raise ValueError('transaction<%s> not found' % kwargs.get('guid'))
        kwargs = self.map(**kwargs)
        for k, v in kwargs.items():
            setattr(transaction, k, v)
        return transaction
