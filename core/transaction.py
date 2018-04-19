# -*- coding:utf-8 -*-
from sqlalchemy import func, distinct
from piecash.core import Transaction, Split

from .base import BaseManager


class TransactionManager(BaseManager):

    model = Transaction

    def __init__(self, book, *args, **kwargs):
        super(TransactionManager, self).__init__(book)
        self.session = self.book.session

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

    def create(self, **kwargs):
        kwargs['currency'] = self.book.default_currency
        kwargs.pop('splits', [])
        transaction = Transaction(**kwargs)
        return transaction

    def alter(self, transaction, **kwargs):
        kwargs.pop('splits', [])
        kwargs.pop('currency', None)
        for k, v in kwargs.items():
            setattr(transaction, k, v)
