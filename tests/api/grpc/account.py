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
