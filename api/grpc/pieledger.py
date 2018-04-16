# -*- coding:utf-8 -*-
from piecash.core import Account
import grpc
from sqlalchemy import exc

from core.book import open_book
from core.account import AccountManager
from core.transaction import TransactionManager

from . import ledger_pb2
from . import services_pb2_grpc
from .mappers import account_mapper, account_model_mapper, \
    transaction_model_mapper


class PieLedger(services_pb2_grpc.PieLedgerServicer):

    def FindOrCreateAccount(self, request, context):
        with open_book() as book:
            acc_mgr = AccountManager(book)
            meta = dict(context.invocation_metadata())
            if request.guid:
                account = acc_mgr.find_by_guid(guid=request.guid)
                if not account:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details("account %s not found" % request.guid)
            else:
                try:
                    account = acc_mgr.find_by_parent(
                        request.parent.guid, request.name,
                        ledger_pb2.AccountType.Name(request.type))
                    if not account:
                        # Start nested session as a commit will be emited,
                        # which validates the account against the book
                        with book.session.begin_nested():
                            account = acc_mgr.create_account(
                                **account_model_mapper.map(request))
                except ValueError as e:
                    context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                    context.set_details(e.args[0])

            ret = account_mapper.map(account)

            # Update balance if required
            if account and meta.get('with_balance', False):
                ret.balance.value = str(account.get_balance(as_decimal=True))

            book.save()
            return ret

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
