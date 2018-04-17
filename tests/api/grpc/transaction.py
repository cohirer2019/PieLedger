# -*- coding:utf-8 -*-
from datetime import datetime, timedelta

import grpc
from piecash.core import Split

from api.grpc import ledger_pb2, services_pb2
from .base import PieLedgerGrpcTest


class TransactionTest(PieLedgerGrpcTest):

    def test_find_transactions(self):

        book = self.book
        acc1 = self.make_account('Acc 1', 'ASSET')
        book.save()
        accid = acc1.guid

        response, result = self.unary_stream(
            'FindTransactions', services_pb2.TransactionQueryRequest(
                guids=['123456', '1qaz', '2wsx'],
                account=ledger_pb2.Account(guid=accid),
                page_number=1,
                result_per_page=1))

        self.assertIs(result.code, grpc.StatusCode.NOT_FOUND)

        acc2 = self.make_account('Acc 2', 'ASSET')
        transaction1 = self.transfer(
            acc1, acc2, 12, datetime.now() - timedelta(minutes=2))
        book.save()
        transactionid1 = transaction1.guid

        response, result = self.unary_stream(
            'FindTransactions', services_pb2.TransactionQueryRequest(
                guids=[transactionid1],
                account=ledger_pb2.Account(guid=accid),
                page_number=0,
                result_per_page=1))

        self.assertEqual(next(response).guid, transactionid1)
        self.assertIs(result.code, grpc.StatusCode.OK)

        transaction2 = self.transfer(
            acc1, acc2, 15, datetime.now() - timedelta(minutes=1))
        transaction3 = self.transfer(acc1, acc2, 20, datetime.now())
        transaction3.splits.extend(
            [Split(account=acc1, value=25), Split(account=acc2, value=-25)])
        book.save()
        transactionid2 = transaction2.guid
        transactionid3 = transaction3.guid

        response, result = self.unary_stream(
            'FindTransactions', services_pb2.TransactionQueryRequest(
                guids=[transactionid1, transactionid2, transactionid3],
                account=ledger_pb2.Account(guid=accid),
                page_number=1,
                result_per_page=1))

        intinal_metadata = result.intinal_metadata
        metadata = dict((x, y) for x, y in intinal_metadata)
        self.assertEqual(metadata.get('num'), 3)
        self.assertEqual(next(response).guid, transactionid2)
        self.assertIs(result.code, grpc.StatusCode.OK)
