# -*- coding:utf-8 -*-
from piecash.core import Account

from core.book import open_book
from mappers import account_mapper
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
                ret = account_mapper.map(account)
                ret.balance = 100
                return ret
