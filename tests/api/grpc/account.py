# -*- coding:utf-8 -*-
import grpc

from api.grpc import ledger_pb2
from api.grpc.mappers import account_mapper
from .base import PieLedgerGrpcTest


class GrpcAccountTest(PieLedgerGrpcTest):

    def test_update_balance(self):
        acc = self.make_account('balance', 'ASSET')
        self.book.save()

        response, result = self.unary_unary(
            'UpdateBalance', account_mapper.map(acc))

        self.assertEqual(response.balance, 100)
        self.assertIs(result.code, grpc.StatusCode.OK)

    def test_findorcreate_account(self):

        # guid找不到account，返回not found
        _, result = self.unary_unary(
            'FindOrCreateAccount', ledger_pb2.Account(guid='123456'))
        self.assertIs(result.code, grpc.StatusCode.NOT_FOUND)

        book = self.book
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
