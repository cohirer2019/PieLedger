# -*- coding:utf-8 -*-
from piecash.core import Transaction, Split

from .base import BaseManager


class TransactionManager(BaseManager):

    def __init__(self, book, *args, **kwagrs):
        super(TransactionManager, self).__init__(book)
        self.session = self.book.session

    def find_transaction(self, guids, account, page_number, result_per_page):
        transactions = self.session.query(Transaction).join(
            Split, Split.transaction_guid == Transaction.guid
        ).filter(
            Transaction.guid.in_(guids),
            Split.account_guid == account.guid
        ).order_by(Transaction.enter_date).group_by(Transaction.guid)
        transactions_page = transactions.offset(
            page_number * result_per_page).limit(result_per_page).all()
        return transactions_page, transactions.count()
