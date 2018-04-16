# -*- coding:utf-8 -*-
from api.grpc import ledger_pb2
from piecash.core import Transaction

from .base import BaseManager


class TransactionManager(BaseManager):

    def __init__(self, book, *args, **kwagrs):
        super(TransactionManager, self).__init__(book)
        self.session = self.book.session

    def find_transaction(self, guids, account, page_number, result_per_page):
        acc_tra = []
        transactions = self.session.query(Transaction).filter(
            Transaction.guid.in_(guids)).offset(0).limit(
                page_number * result_per_page)
        if transactions:
            for transaction in transactions:
                for split in transaction.splits:
                    if split.account.guid == account.guid:
                        acc_tra.append(transaction)
        return acc_tra
