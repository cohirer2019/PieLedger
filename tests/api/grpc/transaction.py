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

    def test_create_transaction(self):
        book = self.book
        acc1 = self.make_account('Acc 1', 'ASSET')
        acc2 = self.make_account('Acc 2', 'ASSET')
        book.save()

        response, result = self.unary_unary(
            'CreateTransaction', ledger_pb2.Transaction(
                reference='10',
                splits=[
                    ledger_pb2.Split(
                        account=ledger_pb2.Account(guid=acc1.guid),
                        amount=ledger_pb2.MonetaryAmount(
                            value='5',
                            num=500,
                            denom=100),
                        memo='use CNY paid'
                    ),
                    ledger_pb2.Split(
                        account=ledger_pb2.Account(guid=acc2.guid),
                        amount=ledger_pb2.MonetaryAmount(
                            value='-5',
                            num=-500,
                            denom=100),
                        memo='use CNY paid')
                ],
                description='CV_paid'
            ))
        self.assertIsNotNone(response.guid)
        self.assertIs(result.code, grpc.StatusCode.OK)

        response, result = self.unary_unary(
            'CreateTransaction', ledger_pb2.Transaction(
                reference='10',
                splits=[
                    ledger_pb2.Split(
                        account=ledger_pb2.Account(guid=acc1.guid),
                        amount=ledger_pb2.MonetaryAmount(
                            value='10',
                            num=500,
                            denom=100),
                        memo='use CNY paid'
                    ),
                    ledger_pb2.Split(
                        account=ledger_pb2.Account(guid=acc2.guid),
                        amount=ledger_pb2.MonetaryAmount(
                            value='-5',
                            num=-500,
                            denom=100),
                        memo='use CNY paid')
                ],
                description='CV_paid'
            ))
        self.assertIs(result.code, grpc.StatusCode.INVALID_ARGUMENT)
        self.assertIn('not balanced on its value', result.detail)
        self.assertIsNone(response)

        response, result = self.unary_unary(
            'CreateTransaction', ledger_pb2.Transaction(
                reference='10',
                splits=[
                    ledger_pb2.Split(
                        account=ledger_pb2.Account(guid=acc1.guid),
                        amount=ledger_pb2.MonetaryAmount(
                            value='10',
                            num=500,
                            denom=100),
                        memo='use CNY paid'
                    ),
                    ledger_pb2.Split(
                        account=ledger_pb2.Account(guid=acc2.guid),
                        amount=ledger_pb2.MonetaryAmount(
                            value='-5',
                            num=-500,
                            denom=100),
                        memo='use CNY paid'),
                    ledger_pb2.Split(
                        account=ledger_pb2.Account(guid=acc2.guid),
                        amount=ledger_pb2.MonetaryAmount(
                            value='-5',
                            num=-500,
                            denom=100),
                        memo='use CNY paid')
                ],
                description='CV_paid'
            ))
        self.assertIsNotNone(response.guid)
        self.assertIs(result.code, grpc.StatusCode.OK)

        response, result = self.unary_unary(
            'CreateTransaction', ledger_pb2.Transaction(
                reference='10',
                splits=[
                    ledger_pb2.Split(
                        account=ledger_pb2.Account(guid='1qaz2wsx'),
                        amount=ledger_pb2.MonetaryAmount(
                            value='10',
                            num=500,
                            denom=100),
                        memo='use CNY paid'
                    ),
                    ledger_pb2.Split(
                        account=ledger_pb2.Account(guid=acc2.guid),
                        amount=ledger_pb2.MonetaryAmount(
                            value='-5',
                            num=-500,
                            denom=100),
                        memo='use CNY paid'),
                    ledger_pb2.Split(
                        account=ledger_pb2.Account(guid=acc2.guid),
                        amount=ledger_pb2.MonetaryAmount(
                            value='-5',
                            num=-500,
                            denom=100),
                        memo='use CNY paid')
                ],
                description='CV_paid'
            ))
        self.assertIs(result.code, grpc.StatusCode.INVALID_ARGUMENT)
        self.assertEqual('account not exist', result.detail)

    def test_alter_transaction(self):
        book = self.book
        acc1 = self.make_account('Acc 1', 'ASSET')
        acc2 = self.make_account('Acc 2', 'ASSET')
        book.save()
        transaction = self.transfer(acc1, acc2, 12)
        book.save()
        transactionid = transaction.guid
        splitid1 = transaction.splits[0].guid
        splitid2 = transaction.splits[1].guid

        response, result = self.unary_unary(
            'AlterTransaction', ledger_pb2.Transaction(
                guid=transactionid,
                reference='10',
                splits=[
                    ledger_pb2.Split(
                        guid=splitid1,
                        account=ledger_pb2.Account(guid=acc1.guid),
                        amount=ledger_pb2.MonetaryAmount(
                            value='50'),
                        memo='use CNY paid'),
                    ledger_pb2.Split(
                        guid=splitid2,
                        account=ledger_pb2.Account(guid=acc2.guid),
                        amount=ledger_pb2.MonetaryAmount(
                            value='-50'),
                        memo='use CNY paid'),
                    ledger_pb2.Split(
                        account=ledger_pb2.Account(guid=acc1.guid),
                        amount=ledger_pb2.MonetaryAmount(
                            value='5'),
                        memo='use CNY paid'
                    ),
                    ledger_pb2.Split(
                        account=ledger_pb2.Account(guid=acc2.guid),
                        amount=ledger_pb2.MonetaryAmount(
                            value='-5'),
                        memo='use CNY paid')
                ],
                description='CV_paid'
            ))
        self.assertEqual(response.guid, transactionid)
        self.assertEqual('use CNY paid', response.splits[0].memo)
        self.assertEqual(4, len(response.splits))
        self.assertIs(result.code, grpc.StatusCode.OK)
