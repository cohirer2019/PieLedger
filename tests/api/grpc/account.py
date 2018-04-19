# -*- coding:utf-8 -*-
import grpc

from api.grpc import ledger_pb2
from api.grpc.mappers import account_mapper
from .base import PieLedgerGrpcTest
from ...core.base import book_context


class GrpcAccountTest(PieLedgerGrpcTest):

    @book_context
    def test_query_with_balance(self, book):
        """Account balance is fetched per request properly"""

        acc = self.make_account(book, 'balance', 'ASSET')
        acc_1 = self.make_account(book, 'cash', 'CASH')
        book.save()

        # No balance update by default
        response, result = self.unary_unary(
            'FindOrCreateAccount', account_mapper.map(acc))
        self.assertIs(result.code, grpc.StatusCode.OK)
        self.assertIsNone(acc._cached_balance)

        # Update / set balance if required with metadata
        response, result = self.unary_unary(
            'FindOrCreateAccount', account_mapper.map(acc), meta=[
                ('with_balance', True)
            ])
        self.assertIs(result.code, grpc.StatusCode.OK)
        self.assertEqual(response.balance.as_string, '0.00')
        book.session.refresh(acc)
        self.assertEqual(acc._cached_balance, 0)

        # Change the balance
        self.transfer(acc, acc_1, 10)

        # Balance not updated if not requested
        response, result = self.unary_unary(
            'FindOrCreateAccount', account_mapper.map(acc))
        self.assertIs(result.code, grpc.StatusCode.OK)
        self.assertEqual(response.balance.as_string, '')

        # Balance updated if required
        response, result = self.unary_unary(
            'FindOrCreateAccount', account_mapper.map(acc), meta=[
                ('with_balance', True)
            ])
        self.assertIs(result.code, grpc.StatusCode.OK)
        self.assertEqual(response.balance.as_string, '-10.00')

    @book_context
    def test_find_or_create_account(self, book):

        root_account_guid = book.root_account.guid

        # guid找到account，返回account的信息
        response, result = self.unary_unary(
            'FindOrCreateAccount', ledger_pb2.Account(guid=root_account_guid))

        self.assertEqual(response.guid, root_account_guid)
        self.assertIs(result.code, grpc.StatusCode.OK)
        self.assertEqual(len(book.accounts), 0)

        # 没有guid，如果没有account，创建一个并返回创建后的信息
        response, result = self.unary_unary(
            'FindOrCreateAccount',
            ledger_pb2.Account(
                name='test_account',
                type=ledger_pb2.AccountType.Value('INCOME'),
                parent=ledger_pb2.Account(guid=root_account_guid)
            ))

        self.assertEqual(response.name, 'test_account')
        self.assertIs(result.code, grpc.StatusCode.OK)
        self.assertEqual(len(book.accounts), 1)

        # 没有guid，如果有account，直接返回account的信息
        response, result = self.unary_unary(
            'FindOrCreateAccount',
            ledger_pb2.Account(
                name='test_account',
                type=ledger_pb2.AccountType.Value('INCOME'),
                parent=ledger_pb2.Account(guid=root_account_guid)
            ))

        self.assertEqual(response.name, 'test_account')
        self.assertIs(result.code, grpc.StatusCode.OK)
        self.assertEqual(len(book.accounts), 1)

    def test_find_or_create_account_failed(self):

        # guid找不到account，返回not found
        _, result = self.unary_unary(
            'FindOrCreateAccount', ledger_pb2.Account(guid='123456'))
        self.assertIs(result.code, grpc.StatusCode.NOT_FOUND)

        # No parent defined
        response, result = self.unary_unary(
            'FindOrCreateAccount',
            ledger_pb2.Account(
                name='test_account',
                type=ledger_pb2.AccountType.Value('INCOME')
            ))
        self.assertIs(result.code, grpc.StatusCode.INVALID_ARGUMENT)
        self.assertIn('has no parent', result.detail)

        # Non-exist parent
        response, result = self.unary_unary(
            'FindOrCreateAccount',
            ledger_pb2.Account(
                name='test_account',
                type=ledger_pb2.AccountType.Value('INCOME'),
                parent=ledger_pb2.Account(guid='dummy')
            ))
        self.assertIs(result.code, grpc.StatusCode.INVALID_ARGUMENT)
        self.assertIn('not found', result.detail)
