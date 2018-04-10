# -*- coding:utf-8 -*-
import grpc

from api.grpc import ledger_pb2
from .base import GrpcTestCase


class AccountTest(GrpcTestCase):

    def test_update_balance(self):
        rpc = self._real_time_server.invoke_unary_unary(
            self._ledger_service.methods_by_name['UpdateBalance'], (),
            ledger_pb2.Account(name='test'), None)
        response, _, code, __ = rpc.termination()

        self.assertEqual(response.balance, 100)
        self.assertIs(code, grpc.StatusCode.OK)
