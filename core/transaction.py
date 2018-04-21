# -*- coding:utf-8 -*-
from sqlalchemy import func, distinct
from piecash.core import Transaction, Split, Account

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
        mnemonic = kwargs.pop('currency', None)
        if not mnemonic:
            account_guid = kwargs.get('splits')[0].get('account')
            account = self.book.query(Account).get(account_guid)
            if not account:
                raise ValueError('account<%s> not found' % account_guid)
            kwargs['currency'] = account.commodity
        else:
            kwargs['currency'] = self.book.currencies.get(
                mnemonic=mnemonic)
        kwargs.pop('splits', [])
        transaction = Transaction(**kwargs)
        return transaction

    def alter(self, transaction, **kwargs):
        kwargs.pop('splits', [])
        kwargs.pop('currency', None)
        for k, v in kwargs.items():
            setattr(transaction, k, v)
