# -*- coding:utf-8 -*-
import grpc
from piecash.core import Account, Split, Transaction

from core.book import open_book
from api.grpc import ledger_pb2, services_pb2
from .base import PieLedgerGrpcTest


class TransactionTest(PieLedgerGrpcTest):

    def test_find_transactions(self):

        with open_book() as book:
            acc1 = Account('Acc 1', 'ASSET', None, parent=book.root_account)
            book.session.add(acc1)
            book.save()
            accid = acc1.guid

        response, result = self.unary_unary(
            'FindTransactions', services_pb2.TransactionQueryRequest(
                guids=['123456', '1qaz', '2wsx'],
                account=ledger_pb2.Account(guid=accid),
                page_number=1,
                result_per_page=1))

        self.assertIs(result.code, grpc.StatusCode.NOT_FOUND)

        with open_book() as book:
            acc2 = Account('Acc 2', 'ASSET', None, parent=book.root_account)
            transaction = Transaction(
                currency=book.default_currency,
                description='test_transaction',
                splits=[
                    Split(account=acc1, value=12),
                    Split(account=acc2, value=-12)])
            book.add(acc2)
            book.add(transaction)
            book.save()
            transactionid = transaction.guid

        response, result = self.unary_unary(
            'FindTransactions', services_pb2.TransactionQueryRequest(
                guids=[transactionid],
                account=ledger_pb2.Account(guid=accid),
                page_number=1,
                result_per_page=1))

        self.assertIs(result.code, grpc.StatusCode.OK)
