# -*- coding:utf-8 -*-
from piecash.core import Account
import grpc

from core.book import open_book
from core.account import AccountManager
from core.transaction import TransactionManager

from .mappers import account_mapper, account_model_mapper, \
    transaction_model_mapper
from . import ledger_pb2
from . import services_pb2_grpc


class PieLedger(services_pb2_grpc.PieLedgerServicer):

    def FindOrCreateAccount(self, request, context):
        with open_book() as book:
            request_args = account_model_mapper.map(request)
            acc_mgr = AccountManager(book)
            if request_args.get('guid'):
                account = acc_mgr.find_by_guid(guid=request_args.get('guid'))
                if not account:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details("account %s not found" % request.guid)
                    return ledger_pb2.Account()
                return account_mapper.map(account)
            else:
                account_parent = acc_mgr.find_by_guid(
                    request_args.get('parent_guid'))
                if not account_parent:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details("account %s not found" % request.guid)
                    return ledger_pb2.Account()
                account = acc_mgr.find_by_parent(
                    account_parent, request_args.get('name'),
                    request_args.get('type'))
                if not account:
                    account = acc_mgr.create_account(
                        account_parent, **request_args)
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

    def FindTransations(self, request, context):
        with open_book() as book:
            request_args = transaction_model_mapper.map(request)
            trans_mgr = TransactionManager(book, **request_args)
            transaction = trans_mgr.find_transaction()
