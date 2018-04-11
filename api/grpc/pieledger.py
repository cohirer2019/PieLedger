# -*- coding:utf-8 -*-
from piecash.core import Account
import grpc

from core.book import open_book
import ledger_pb2
import services_pb2_grpc


class PieLedger(services_pb2_grpc.PieLedgerServicer):
    def FindOrCreateAccount(self, request, context):
        with open_book() as book:
            if request.guid:
                account = book.session.query(Account).filter(
                    Account.guid == request.guid).first()
                if not account:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details("account %s not found" % request.guid)
                    return ledger_pb2.Account()
                return ledger_pb2.Account(
                    guid=account.guid,
                    name=account.name,
                    type=account.type,
                    parent=account.parent,
                    placeholder=account.placeholder)
            else:
                account_parent = book.session.query(Account).filter(
                    Account.guid == request.parent.guid).first()
                account = book.session.query(Account).filter(
                    Account.name == request.name,
                    Account.parent == account_parent,
                    Account.type == ledger_pb2.AccountType.Name(request.type)
                ).first()
                if not account:
                    EUR = book.commodities.get(mnemonic="EUR")
                    account = Account(
                        name=request.name,
                        type=ledger_pb2.AccountType.Name(request.type),
                        commodity=EUR,
                        parent=account_parent,
                        placeholder=request.placeholder)
                    book.save()
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
