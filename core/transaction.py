# -*- coding:utf-8 -*-
from sqlalchemy import func, distinct
from piecash.core import Account, Transaction, Split

from .base import BaseManager


class TransactionManager(BaseManager):

    def __init__(self, book, *args, **kwargs):
        super(TransactionManager, self).__init__(book)
        self.session = self.book.session

    def map_splits(self, model, data):
        splits_to_keep = {s.guid: s for s in data if s.get('guid')}
        new_splits = [s for s in data if not s.get('guid')]
        for split in model:
            if split.guid not in splits_to_keep.keys():
                self.book.delete(split)
                continue
            for k, v in splits_to_keep[split.guid]:
                setattr(split, k, v)
        for s_data in new_splits:
            s_data['account'] = \
                self.book.query(Account).get(s_data.pop('account'))
            if not s_data['account']:
                raise ValueError('account not exist')
            model.append(Split(**s_data))

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
        splits_data = kwargs.pop('splits', [])
        transaction = Transaction(**kwargs)
        self.map_splits(transaction.splits, splits_data)
        return transaction

    def alter_transaction(self, transaction, **kwargs):
        self.map_splits(transaction.splits, kwargs.pop('splits', []))
        for k, v in kwargs.items():
            setattr(transaction, k, v)
