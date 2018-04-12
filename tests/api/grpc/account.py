# -*- coding:utf-8 -*-
import grpc
from piecash.core import Account

from core.book import open_book
from api.grpc import ledger_pb2
from .base import PieLedgerGrpcTest


class AccountTest(PieLedgerGrpcTest):

    def test_update_balance(self):

        with open_book() as book:
            acc = Account('balance', 'ASSET', None, parent=book.root_account)
            book.session.add(acc)
            book.save()
            accid = acc.guid

        response, result = self.unary_unary(
            'UpdateBalance', ledger_pb2.Account(guid=accid))

        self.assertEqual(response.balance, 100)
        self.assertIs(result.code, grpc.StatusCode.OK)

    def test_findorcreate_account(self):

        # guid找不到account，返回not found
        _, result = self.unary_unary(
            'FindOrCreateAccount', ledger_pb2.Account(guid='123456'))
        self.assertIs(result.code, grpc.StatusCode.NOT_FOUND)

        with open_book() as book:
            root_account_guid = book.root_account.guid
            book_count = len(book.accounts)

        # guid找到account，返回account的信息
        response, result = self.unary_unary(
            'FindOrCreateAccount', ledger_pb2.Account(guid=root_account_guid))

        self.assertEqual(response.guid, root_account_guid)
        self.assertIs(result.code, grpc.StatusCode.OK)

        # 没有guid，如果没有account，创建一个并返回创建后的信息
        response, result = self.unary_unary(
            'FindOrCreateAccount',
            ledger_pb2.Account(
                guid=None,
                name='test_account',
                type=ledger_pb2.AccountType.Value('INCOME'),
                parent=ledger_pb2.Account(guid=root_account_guid)
            ))

        self.assertEqual(response.name, 'test_account')
        self.assertIs(result.code, grpc.StatusCode.OK)
        with open_book() as book:
            root_account_guid = book.root_account.guid
            book_count_new = len(book.accounts)
        self.assertEqual(book_count + 1, book_count_new)

        # 没有guid，如果有account，直接返回account的信息
        response, result = self.unary_unary(
            'FindOrCreateAccount',
            ledger_pb2.Account(
                guid=None,
                name='test_account',
                type=ledger_pb2.AccountType.Value('INCOME'),
                parent=ledger_pb2.Account(guid=root_account_guid)
            ))

        self.assertEqual(response.name, 'test_account')
        self.assertIs(result.code, grpc.StatusCode.OK)
        with open_book() as book:
            root_account_guid = book.root_account.guid
            book_count_new = len(book.accounts)
        self.assertEqual(book_count + 1, book_count_new)
