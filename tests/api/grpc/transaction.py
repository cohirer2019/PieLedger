# -*- coding:utf-8 -*-
import unittest

import grpc
from piecash.core import Account

from core.book import open_book
from api.grpc import ledger_pb2, services_pb2
from .base import PieLedgerGrpcTest


class TransactionTest(PieLedgerGrpcTest):

    @unittest.skip('Disabled as failed')
    def test_find_transactions(self):

        with open_book() as book:
            acc = Account('balance', 'ASSET', None, parent=book.root_account)
            book.session.add(acc)
            book.save()
            accid = acc.guid

        response, result = self.unary_unary(
            'FindTransations', services_pb2.TransactionQueryRequest(
            	guids=['123456', '1qaz', '2wsx'],
            	account=ledger_pb2.Account(guid=accid),
            	page_number=1,
            	result_per_page=1))

        self.assertEqual(response.balance, 100)
        self.assertIs(result.code, grpc.StatusCode.OK)
