# -*- coding:utf-8 -*-
from datetime import datetime, timedelta
from decimal import Decimal

import grpc
from google.protobuf.timestamp_pb2 import Timestamp

from pieledger.api.grpc import services_pb2, ledger_pb2
from tests.core.base import book_context
from .base import PieLedgerGrpcTest


class GrpcSplitTest(PieLedgerGrpcTest):

    @book_context
    def test_find_splits(self, book):
        acc1 = self.make_account(book, 'Acc 1', 'ASSET')
        acc2 = self.make_account(book, 'Acc 2', 'CASH')
        acc1_child = self.make_account(
            book, 'Acc 1 child', 'ASSET', parent=acc1)

        ROUNDS = 5
        for r in range(ROUNDS):
            enter_date = datetime.now() + timedelta(minutes=r)
            trans = self.transfer(acc1, acc2, r*2, enter_date=enter_date)
            trans.description = 'Round %s main transfer' % r
            trans.splits[0].action = 'B'
            trans.splits[0].memo = 'with discount'
            book.flush()
            trans = self.transfer(
                acc1_child, acc2, r*2+1,
                enter_date=enter_date+timedelta(seconds=1))
            trans.description = 'Round %s sub transfer' % r
            trans.num = 'X20180420%s' % r
            trans.splits[0].action = 'share'
            book.flush()
        book.save()

        # Query for child account
        response, result = self.unary_stream(
            'FindSplits', services_pb2.SplitQueryRequest(
                account=ledger_pb2.Account(guid=acc1_child.guid)))
        self.assertEqual(result.code, grpc.StatusCode.OK)
        initial_metadata = dict(result.initial_metadata)
        self.assertEqual(int(initial_metadata.get('total')), ROUNDS)

        # Request for parent account
        response, result = self.unary_stream(
            'FindSplits', services_pb2.SplitQueryRequest(
                account=ledger_pb2.Account(guid=acc1.guid)))
        self.assertEqual(result.code, grpc.StatusCode.OK)
        initial_metadata = dict(result.initial_metadata)
        # responses are splits with parent and all child account
        self.assertEqual(int(initial_metadata.get('total')), ROUNDS*2)

        # responses are ordered by enter date desc
        splits = list(response)
        self.assertEqual(
            list(range(-ROUNDS*2+1, 1)),
            [Decimal(s.amount.as_string) for s in splits])

        # Check for serialized info
        self.assertIn('X20180420', splits[0].transaction.reference)
        last_amount = (2*(ROUNDS-1)+1)
        self.assertEqual(Decimal(splits[0].amount.as_string), -last_amount)
        self.assertEqual(
            Decimal(splits[0].running_balance.as_string),
            -sum(range(1, last_amount+1, 2)))
        self.assertEqual(splits[0].custom_action, 'share')
        self.assertEqual(splits[1].standard_action, ledger_pb2.BUY)
        self.assertEqual(splits[1].memo, 'with discount')

        # Paging
        response, result = self.unary_stream(
            'FindSplits', services_pb2.SplitQueryRequest(
                account=ledger_pb2.Account(guid=acc1.guid),
                result_per_page=ROUNDS-1, page_number=2))
        self.assertEqual(result.code, grpc.StatusCode.OK)
        self.assertEqual(len(list(response)), 2)

        # Search by action type
        response, result = self.unary_stream(
            'FindSplits', services_pb2.SplitQueryRequest(
                account=ledger_pb2.Account(guid=acc1.guid),
                standard_action=ledger_pb2.SplitAction.Value('BUY')))
        self.assertEqual(result.code, grpc.StatusCode.OK)
        initial_metadata = dict(result.initial_metadata)
        self.assertEqual(int(initial_metadata.get('total')), ROUNDS)
        self.assertEqual(
            next(response).standard_action, ledger_pb2.BUY)

        # Search by action string
        response, result = self.unary_stream(
            'FindSplits', services_pb2.SplitQueryRequest(
                account=ledger_pb2.Account(guid=acc1.guid),
                custom_action='share'))
        self.assertEqual(result.code, grpc.StatusCode.OK)
        initial_metadata = dict(result.initial_metadata)
        self.assertEqual(int(initial_metadata.get('total')), ROUNDS)
        self.assertEqual(next(response).custom_action, 'share')

        # Search by time
        from_dt = Timestamp()
        from_dt.FromDatetime(enter_date)
        response, result = self.unary_stream(
            'FindSplits', services_pb2.SplitQueryRequest(
                account=ledger_pb2.Account(guid=acc1.guid),
                from_datetime=from_dt))
        self.assertEqual(result.code, grpc.StatusCode.OK)
        initial_metadata = dict(result.initial_metadata)
        self.assertEqual(int(initial_metadata.get('total')), 2)

        # Search by account name
        response, result = self.unary_stream(
            'FindSplits', services_pb2.SplitQueryRequest(
                account=ledger_pb2.Account(),
                account_name='credit'))
        self.assertEqual(result.code, grpc.StatusCode.OK)
        self.assertEqual(len(list(response)), 0)

        response, result = self.unary_stream(
            'FindSplits', services_pb2.SplitQueryRequest(
                account=ledger_pb2.Account(),
                account_name='Acc 1'))
        self.assertEqual(result.code, grpc.StatusCode.OK)
        self.assertEqual(len(list(response)), 5)

        # Search by transaction reference
        response, result = self.unary_stream(
            'FindSplits', services_pb2.SplitQueryRequest(
                account=ledger_pb2.Account(),
                transref='X201804201'))
        self.assertEqual(result.code, grpc.StatusCode.OK)
        self.assertEqual(len(list(response)), 2)

        # Search by transaction split guid
        response, result = self.unary_stream(
            'FindSplits', services_pb2.SplitQueryRequest(
                guid='fake_guid'))
        self.assertEqual(result.code, grpc.StatusCode.OK)
        self.assertEqual(len(list(response)), 0)

        response, result = self.unary_stream(
            'FindSplits', services_pb2.SplitQueryRequest(
                guid=trans.splits[0].guid))
        self.assertEqual(result.code, grpc.StatusCode.OK)
        split = next(response)
        self.assertEqual(split.guid, trans.splits[0].guid)
        self.assertEqual(split.account.guid, trans.splits[0].account.guid)
        self.assertEqual(
            split.transaction.guid, trans.splits[0].transaction.guid)

        # Search by inverse account id
        response, result = self.unary_stream(
            'FindSplits', services_pb2.SplitQueryRequest(
                inverse_acc_id=acc1_child.guid))
        self.assertEqual(result.code, grpc.StatusCode.OK)
        self.assertEqual(len(list(response)), 5)

    @book_context
    def test_find_splits_failed(self, book):
        # Account is required
        _, result = self.unary_stream(
            'FindSplits', services_pb2.SplitQueryRequest(
                account=ledger_pb2.Account(guid='dummy')))
        self.assertEqual(result.code, grpc.StatusCode.INVALID_ARGUMENT)
        self.assertIn('not found', result.detail)

    @book_context
    def test_find_with_inverses(self, book):
        acc1 = self.make_account(book, 'Acc 1', 'ASSET')
        acc2 = self.make_account(book, 'Acc 2', 'CASH')

        self.transfer(acc1, acc2, 100)
        book.save()

        # Default query returns no inverses
        response, result = self.unary_stream(
            'FindSplits', services_pb2.SplitQueryRequest(
                account=ledger_pb2.Account(guid=acc1.guid)))
        self.assertEqual(result.code, grpc.StatusCode.OK)
        self.assertFalse(next(response).inverses)

        # Query with inverse in metadata
        response, result = self.unary_stream(
            'FindSplits', services_pb2.SplitQueryRequest(
                account=ledger_pb2.Account(guid=acc1.guid)),
            meta=(('inverse', 'true'),))
        self.assertEqual(result.code, grpc.StatusCode.OK)
        inverses = next(response).inverses
        self.assertEqual(len(inverses), 1)
        self.assertEqual(inverses[0].account.guid, acc2.guid)
