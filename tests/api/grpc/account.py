# -*- coding:utf-8 -*-
import grpc

from pieledger.api.grpc import ledger_pb2
from pieledger.api.grpc.mappers import account_mapper

from core.base import book_context
from .base import PieLedgerGrpcTest


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

        self.assertIs(result.code, grpc.StatusCode.OK)
        self.assertEqual(response.guid, root_account_guid)
        self.assertEqual(len(book.accounts), 0)

        # 没有guid，如果没有account，创建一个并返回创建后的信息
        response, result = self.unary_unary(
            'FindOrCreateAccount',
            ledger_pb2.Account(
                name='test_account',
                currency='CNY',
                type=ledger_pb2.AccountType.Value('INCOME'),
                parent=ledger_pb2.Account(guid=root_account_guid)
            ))

        self.assertIs(result.code, grpc.StatusCode.OK)
        self.assertEqual(response.name, 'test_account')
        self.assertEqual(len(book.accounts), 1)
        self.assertEqual(book.accounts[0].commodity.mnemonic, 'CNY')

        # 没有guid，如果有account，直接返回account的信息
        response, result = self.unary_unary(
            'FindOrCreateAccount',
            ledger_pb2.Account(
                name='test_account',
                type=ledger_pb2.AccountType.Value('INCOME'),
                parent=ledger_pb2.Account(guid=root_account_guid)
            ))

        self.assertIs(result.code, grpc.StatusCode.OK)
        self.assertEqual(response.name, 'test_account')
        self.assertEqual(len(book.accounts), 1)

        # 如果是placeholder不为True且没有parent account，报错
        response, result = self.unary_unary(
            'FindOrCreateAccount',
            ledger_pb2.Account(
                name='test_account',
                type=ledger_pb2.AccountType.Value('INCOME'),
            ))

        self.assertIs(result.code, grpc.StatusCode.INVALID_ARGUMENT)
        self.assertIn('has no parent', result.detail)

        # 没有guid，如果有account，直接返回account的信息
        response, result = self.unary_unary(
            'FindOrCreateAccount',
            ledger_pb2.Account(
                name='test_account',
                type=ledger_pb2.AccountType.Value('INCOME'),
                placeholder=True
            ))

        self.assertIs(result.code, grpc.StatusCode.OK)
        self.assertEqual(response.name, 'test_account')
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

        # No parent defined but is placeholder
        response, result = self.unary_unary(
            'FindOrCreateAccount',
            ledger_pb2.Account(
                placeholder=True,
                name='test_account',
                type=ledger_pb2.AccountType.Value('INCOME')
            ))
        self.assertIs(result.code, grpc.StatusCode.OK)
        self.assertIn('Root Account', response.parent.name)

        # Invalid currency
        response, result = self.unary_unary(
            'FindOrCreateAccount',
            ledger_pb2.Account(
                name='test_account',
                currency='dummy',
                type=ledger_pb2.AccountType.Value('INCOME')
            ))
        self.assertIs(result.code, grpc.StatusCode.INVALID_ARGUMENT)
        self.assertIn('Could not find the ISO code', result.detail)

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
