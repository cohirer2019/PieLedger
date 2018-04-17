# -*- coding:utf-8 -*-
from piecash.core import Account
import grpc

from core.book import open_book
from core.account import AccountManager
from core.transaction import TransactionManager
from .mappers import account_mapper, account_model_mapper, \
    transaction_mapper, transaction_model_mapper
from . import ledger_pb2
from . import services_pb2_grpc


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

    def FindTransactions(self, request, context):
        with open_book() as book:
            trans_mgr = TransactionManager(book)
            transactions, num = trans_mgr.find_transaction(
                request.guids, request.account, request.page_number,
                request.result_per_page)
            if not transactions:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("transaction %s not found")
                return
            context.send_initial_metadata((('num', num),))
            for transaction in transactions:
                yield transaction_mapper.map(transaction)

    def CreateTransaction(self, request, context):
        with open_book() as book:
            trans_mgr = TransactionManager(book)
            transaction = trans_mgr.create_transaction(
                **transaction_model_mapper.map(request))
            return transaction_mapper.map(transaction)
