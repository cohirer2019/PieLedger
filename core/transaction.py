# -*- coding:utf-8 -*-
from sqlalchemy import func, distinct
from piecash.core import Transaction, Split, Account

from .base import BaseManager


class TransactionManager(BaseManager):

    def __init__(self, book, *args, **kwagrs):
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

    def create_transaction(self, **kwagrs):
        splits = kwagrs.pop('splits')
        kwagrs['splits'] = []
        kwagrs['currency'] = self.book.default_currency
        for split in splits:
            account_guid = split.pop('account')
            split['account'] = self.book.query(Account).get(account_guid)
            kwagrs['splits'].append(Split(**split))
        return Transaction(**kwagrs)
