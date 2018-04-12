# -*- coding:utf-8 -*-
from api.grpc import ledger_pb2
from piecash.core import Account

from base import BaseManager


class AccountManager(BaseManager):

    def __init__(self, book, *args, **kwargs):
        super(AccountManager, self).__init__(book)
        self.guid = kwargs.get('guid')
        self.name = kwargs.get('name')
        self.type = kwargs.get('type')
        self.placeholder = kwargs.get('placeholder')
        self.parent = self.session.query(Account).filter(
            Account.guid == kwargs.get('parent', {}).get('guid')).first()

    def find_account(self):
        if self.guid:
            account = self.session.query(Account).filter(
                Account.guid == self.guid).first()
            if account:
                return account, 'ok'
            return None, 'not found'
        else:
            account = self.session.query(Account).filter(
                Account.name == self.name,
                Account.parent == self.parent,
                Account.type == ledger_pb2.AccountType.Name(self.type)
            ).first()
            if account:
                return account, 'ok'
        return None, 'create'

    def create_account(self):
        EUR = self.book.commodities.get(mnemonic="EUR")
        account = Account(
            name=self.name,
            type=ledger_pb2.AccountType.Name(self.type),
            commodity=EUR,
            parent=self.parent,
            placeholder=self.placeholder)
        self.book.save()
        return account
