# -*- coding:utf-8 -*-
from piecash.core import Account

from core.book import open_book
import ledger_pb2
import services_pb2_grpc


class PieLedger(services_pb2_grpc.PieLedgerServicer):

    def FindOrCreateAccount(self, request, context):
        return ledger_pb2.Account(name='%s' % request.name)

    def UpdateBalance(self, request, context):
        with open_book() as book:
            account = book.session.query(Account).filter(
                Account.guid == request.guid
            ).first()
            if account:
                return ledger_pb2.Account(
                    guid=account.guid,
                    name=account.name,
                    balance=100
                )
