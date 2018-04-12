# -*- coding:utf-8 -*-
from api.grpc import ledger_pb2
from piecash.core import Transaction

from base import BaseManager


class TransactionManager(BaseManager):

    def __init__(self, book, *args, **kwagrs):
        super(TransactionManager, self).__init__(book)
        self.session = self.book.session
        self.guid = kwagrs.get('guid')
        self.reference = kwagrs.get('reference')
        self.description = kwagrs.get('description')
        self.account = kwagrs.get('account')
        self.page_number = kwagrs.get('account')
        self.result_per_page = kwagrs.get('result_per_page')

    def find_transaction(self):
        transaction = self.session.query(Transaction).filter(
            Transaction.guid.in_(self.guid)).offset
        if transaction:
            return transaction, 'ok'
        return None, 'not found'
