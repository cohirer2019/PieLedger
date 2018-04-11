# -*- coding:utf-8 -*-
import grpc
from piecash.core import Account

from core.book import open_book
from api.grpc import ledger_pb2
from .base import GrpcTestCase


class AccountTest(GrpcTestCase):

    def test_update_balance(self):

        with open_book() as book:
            acc = Account('balance', 'ASSET', None, parent=book.root_account)
            book.session.add(acc)
            book.save()
            accid = acc.guid

        rpc = self._real_time_server.invoke_unary_unary(
            self._ledger_service.methods_by_name['UpdateBalance'], (),
            ledger_pb2.Account(guid=accid), None)
        response, _, code, __ = rpc.termination()

        self.assertEqual(response.balance, 100)
        self.assertIs(code, grpc.StatusCode.OK)

    def test_findorcreate_account(self):

        # guid找不到account，返回not found
        rpc = self._real_time_server.invoke_unary_unary(
            self._ledger_service.methods_by_name['FindOrCreateAccount'], (),
            ledger_pb2.Account(guid='123456'), None)
        response, _, code, __ = rpc.termination()

        self.assertIs(code, grpc.StatusCode.NOT_FOUND)

        with open_book() as book:
            root_account_guid = book.root_account.guid
            book_count = len(book.accounts)

        # guid找到account，返回account的信息
        rpc = self._real_time_server.invoke_unary_unary(
            self._ledger_service.methods_by_name['FindOrCreateAccount'], (),
            ledger_pb2.Account(guid=root_account_guid), None)
        response, _, code, __ = rpc.termination()

        self.assertEqual(response.guid, root_account_guid)
        self.assertIs(code, grpc.StatusCode.OK)

        # 没有guid，如果没有account，创建一个并返回创建后的信息
        rpc = self._real_time_server.invoke_unary_unary(
            self._ledger_service.methods_by_name['FindOrCreateAccount'], (),
            ledger_pb2.Account(
                guid=None,
                name='test_account',
                type=ledger_pb2.AccountType.Value('INCOME'),
                parent=ledger_pb2.Account(guid=root_account_guid)
            ), None)
        response, _, code, __ = rpc.termination()

        self.assertEqual(response.name, 'test_account')
        self.assertIs(code, grpc.StatusCode.OK)
        with open_book() as book:
            root_account_guid = book.root_account.guid
            book_count_new = len(book.accounts)
        self.assertEqual(book_count + 1, book_count_new)

        # 没有guid，如果有account，直接返回account的信息
        rpc = self._real_time_server.invoke_unary_unary(
            self._ledger_service.methods_by_name['FindOrCreateAccount'], (),
            ledger_pb2.Account(
                guid=None,
                name='test_account',
                type=ledger_pb2.AccountType.Value('INCOME'),
                parent=ledger_pb2.Account(guid=root_account_guid)
            ), None)
        response, _, code, __ = rpc.termination()

        self.assertEqual(response.name, 'test_account')
        self.assertIs(code, grpc.StatusCode.OK)
        with open_book() as book:
            root_account_guid = book.root_account.guid
            book_count_new = len(book.accounts)
        self.assertEqual(book_count + 1, book_count_new)
