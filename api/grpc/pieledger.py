# -*- coding:utf-8 -*-
from protobuf_to_dict import protobuf_to_dict
from piecash.core import Account
import grpc

from core.book import open_book
from core.account import AccountManager, TransactionManager
from mappers import account_mapper
import ledger_pb2
import services_pb2_grpc


class PieLedger(services_pb2_grpc.PieLedgerServicer):
    def FindOrCreateAccount(self, request, context):
        with open_book() as book:
            request_args = protobuf_to_dict(request)
            acc_mgr = AccountManager(book, **request_args)
            account, msg = acc_mgr.find_account()
            if msg == 'not found':
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("account %s not found" % request.guid)
                return ledger_pb2.Account()
            elif msg == 'create':
                account = acc_mgr.create_account()
            return account_mapper.map(account)

    def UpdateBalance(self, request, context):
        with open_book() as book:
            account = book.session.query(Account).filter(
                Account.guid == request.guid
            ).first()
            if account:
                ret = account_mapper.map(account)
                ret.balance = 100
                return ret
