# -*- coding:utf-8 -*-
from datetime import datetime, timedelta

import grpc
from piecash.core import Split

from api.grpc import ledger_pb2, services_pb2
from tests.core.base import book_context
from .base import PieLedgerGrpcTest


class TransactionTest(PieLedgerGrpcTest):

    @book_context
    def test_find_transactions(self, book):

        acc1 = self.make_account(book, 'Acc 1', 'ASSET')
        book.save()
        accid = acc1.guid

        response, result = self.unary_stream(
            'FindTransactions', services_pb2.TransactionQueryRequest(
                guids=['123456', '1qaz', '2wsx'],
                account=ledger_pb2.Account(guid=accid),
                page_number=1,
                result_per_page=1))

        self.assertIs(result.code, grpc.StatusCode.NOT_FOUND)

        acc2 = self.make_account(book, 'Acc 2', 'ASSET')
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

        initial_metadata = result.initial_metadata
        metadata = dict((x, y) for x, y in initial_metadata)
        self.assertEqual(metadata.get('num'), '3')
        self.assertEqual(next(response).guid, transactionid2)
        self.assertIs(result.code, grpc.StatusCode.OK)

    @book_context
    def test_create_transaction(self, book):
        acc1 = self.make_account(book, 'Acc 1', 'ASSET')
        acc2 = self.make_account(book, 'Acc 2', 'ASSET')
        book.save()

        response, result = self.unary_unary(
            'CreateTransaction', ledger_pb2.Transaction(
                reference='10',
                splits=[
                    ledger_pb2.Split(
                        account=ledger_pb2.Account(guid=acc1.guid),
                        amount=ledger_pb2.MonetaryAmount(as_int=5),
                        memo='购买简历'
                    ),
                    ledger_pb2.Split(
                        account=ledger_pb2.Account(guid=acc2.guid),
                        amount=ledger_pb2.MonetaryAmount(as_int=-5),
                        memo='购买简历')
                ],
                description='CV_paid'
            ))
        self.assertIs(result.code, grpc.StatusCode.OK)
        self.assertIsNotNone(response.guid)

        response, result = self.unary_unary(
            'CreateTransaction', ledger_pb2.Transaction(
                reference='10',
                splits=[
                    ledger_pb2.Split(
                        account=ledger_pb2.Account(guid=acc1.guid),
                        amount=ledger_pb2.MonetaryAmount(as_int=10),
                        memo='use CNY paid'
                    ),
                    ledger_pb2.Split(
                        account=ledger_pb2.Account(guid=acc2.guid),
                        amount=ledger_pb2.MonetaryAmount(as_int=10),
                        memo='use CNY paid')
                ],
                description='CV_paid'
            ))
        self.assertIs(result.code, grpc.StatusCode.INVALID_ARGUMENT)
        self.assertIn('not balanced on its value', result.detail)

        response, result = self.unary_unary(
            'CreateTransaction', ledger_pb2.Transaction(
                reference='10',
                splits=[
                    ledger_pb2.Split(
                        account=ledger_pb2.Account(guid=acc1.guid),
                        amount=ledger_pb2.MonetaryAmount(as_int=10),
                        memo='use CNY paid'
                    ),
                    ledger_pb2.Split(
                        account=ledger_pb2.Account(guid=acc2.guid),
                        amount=ledger_pb2.MonetaryAmount(as_int=-5),
                        memo='use CNY paid'),
                    ledger_pb2.Split(
                        account=ledger_pb2.Account(guid=acc2.guid),
                        amount=ledger_pb2.MonetaryAmount(as_int=-5),
                        memo='use CNY paid')
                ],
                description='CV_paid'
            ))
        self.assertIs(result.code, grpc.StatusCode.OK)
        self.assertIsNotNone(response.guid)

        response, result = self.unary_unary(
            'CreateTransaction', ledger_pb2.Transaction(
                reference='10',
                splits=[
                    ledger_pb2.Split(
                        account=ledger_pb2.Account(guid='1qaz2wsx'),
                        amount=ledger_pb2.MonetaryAmount(as_int=10),
                        memo='use CNY paid'
                    ),
                    ledger_pb2.Split(
                        account=ledger_pb2.Account(guid=acc2.guid),
                        amount=ledger_pb2.MonetaryAmount(as_int=-5),
                        memo='use CNY paid'),
                    ledger_pb2.Split(
                        account=ledger_pb2.Account(guid=acc2.guid),
                        amount=ledger_pb2.MonetaryAmount(as_int=-5),
                        memo='use CNY paid')
                ],
                description='CV_paid'
            ))
        self.assertIs(result.code, grpc.StatusCode.INVALID_ARGUMENT)
        self.assertEqual('account<1qaz2wsx> not found', result.detail)

        # split的transaction currency与account currency不同
        response, result = self.unary_unary(
            'CreateTransaction', ledger_pb2.Transaction(
                reference='10',
                currency='JPY',
                splits=[
                    ledger_pb2.Split(
                        account=ledger_pb2.Account(guid=acc1.guid),
                        amount=ledger_pb2.MonetaryAmount(as_int=5),
                        memo='use CNY paid'),
                    ledger_pb2.Split(
                        account=ledger_pb2.Account(guid=acc2.guid),
                        amount=ledger_pb2.MonetaryAmount(as_int=-5),
                        memo='use CNY paid')
                ],
                description='CV_paid'
            ))
        self.assertIs(result.code, grpc.StatusCode.INVALID_ARGUMENT)
        self.assertEqual('currency must identical', result.detail)

    @book_context
    def test_alter_transaction(self, book):
        acc1 = self.make_account(book, 'Acc 1', 'ASSET')
        acc2 = self.make_account(book, 'Acc 2', 'ASSET')
        book.save()
        transaction = self.transfer(acc1, acc2, 12)
        book.save()
        transactionid = transaction.guid

        response, result = self.unary_unary(
            'AlterTransaction', services_pb2.TransactionAlterRequest(
                transaction=ledger_pb2.Transaction(
                    guid=transactionid,
                    reference='10',
                    description='CV_paid'),
                append_splits=[
                    ledger_pb2.Split(
                        account=ledger_pb2.Account(guid=acc1.guid),
                        amount=ledger_pb2.MonetaryAmount(as_int=500),
                        custom_action='withdraw',
                        memo='use CNY paid'),
                    ledger_pb2.Split(
                        account=ledger_pb2.Account(guid=acc2.guid),
                        amount=ledger_pb2.MonetaryAmount(as_int=-500),
                        custom_action='recharge',
                        memo='use CNY paid'),
                    ledger_pb2.Split(
                        account=ledger_pb2.Account(guid=acc1.guid),
                        amount=ledger_pb2.MonetaryAmount(as_string='2.00'),
                        custom_action='withdraw',
                        memo='use CNY paid'),
                    ledger_pb2.Split(
                        account=ledger_pb2.Account(guid=acc2.guid),
                        amount=ledger_pb2.MonetaryAmount(as_string='-2.00'),
                        custom_action='recharge',
                        memo='use CNY paid')
                ]
            ))
        self.assertIs(result.code, grpc.StatusCode.OK)
        self.assertEqual(response.guid, transactionid)
        self.assertEqual(6, len(response.splits))

        response, result = self.unary_unary(
            'AlterTransaction', services_pb2.TransactionAlterRequest(
                transaction=ledger_pb2.Transaction(
                    guid=transactionid,
                    reference='10',
                    description='CV_paid'),
                append_splits=[
                    ledger_pb2.Split(
                        account=ledger_pb2.Account(guid=acc1.guid),
                        amount=ledger_pb2.MonetaryAmount(as_string='2.001'),
                        custom_action='withdraw',
                        memo='use CNY paid'),
                    ledger_pb2.Split(
                        account=ledger_pb2.Account(guid=acc2.guid),
                        amount=ledger_pb2.MonetaryAmount(as_string='-2.001'),
                        custom_action='recharge',
                        memo='use CNY paid')
                ]
            ))
        self.assertIs(result.code, grpc.StatusCode.INVALID_ARGUMENT)
        self.assertEqual(result.detail, 'invalid value range!')
