# -*- coding:utf-8 -*-
import grpc

from core.book import open_book
from core.account import AccountManager
from core.transaction import TransactionManager
from core.split import SplitManager
from .mappers import account_mapper, account_model_mapper, \
    transaction_mapper, transaction_model_mapper, split_model_mapper
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
                        ledger_pb2.AccountType.Name(request.type),
                        request.placeholder)
                    if not account:
                        # Start nested session as a commit will be emited,
                        # which validates the account against the book
                        with book.session.begin_nested():
                            account = acc_mgr.create(
                                currency=request.currency,
                                **account_model_mapper.map(request))
                except ValueError as e:
                    context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                    context.set_details(e.args[0])
            ret = account_mapper.map(account)

            # Update balance if required
            if account and meta.get('with_balance', False):
                ret.balance.as_string = str(account.get_balance())

            book.save()
            return ret

    def FindTransactions(self, request, context):
        with open_book() as book:
            trans_mgr = TransactionManager(book)
            transactions, num = trans_mgr.find_transaction(
                request.guids, request.account.guid, request.page_number,
                request.result_per_page)
            if not transactions:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("transaction %s not found")
                return
            context.send_initial_metadata((('num', str(num)),))
            for transaction in transactions:
                yield transaction_mapper.map(transaction)

    def CreateTransaction(self, request, context):
        with open_book() as book:
            trans_mgr = TransactionManager(book)
            split_mgr = SplitManager(book)
            try:
                transaction = trans_mgr.create(
                    **transaction_model_mapper.map(request))
                for split in request.splits:
                    split_mgr.create(
                        transaction, **split_model_mapper.map(split))
            except ValueError as e:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details(e.args[0])
                return ledger_pb2.Transaction()
            try:
                book.save()
            except Exception as e:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details(e.args[0])
            return transaction_mapper.map(transaction)

    def AlterTransaction(self, request, context):
        with open_book() as book:
            trans_mgr = TransactionManager(book)
            split_mgr = SplitManager(book)
            transaction = trans_mgr.find_by_guid(guid=request.transaction.guid)
            if not transaction:
                context.set_code(grpc.StatusCode.NOT_FOUND)
            try:
                for split in request.append_splits:
                    split_mgr.create(
                        transaction, **split_model_mapper.map(split))
                trans_mgr.alter(
                    transaction,
                    **transaction_model_mapper.map(request.transaction))
            except ValueError as e:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details(e.args[0])
            try:
                book.save()
            except Exception as e:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details(e.args[0])
            return transaction_mapper.map(transaction)
