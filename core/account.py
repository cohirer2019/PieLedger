# -*- coding:utf-8 -*-
from piecash.core import Account

from .base import BaseManager


class AccountManager(BaseManager):

    def find_by_guid(self, guid):
        account = self.session.query(Account).filter(
            Account.guid == guid).first()
        return account

    def find_by_parent(self, parent, name, type):
        account = self.session.query(Account).filter(
            Account.parent == parent,
            Account.name == name,
            Account.type == type).first()
        return account

    def create_account(self, parent, **args):
        args['commodity'] = self.book.commodities.get(mnemonic="EUR")
        args['parent'] = parent
        args.pop('parent_guid')
        account = Account(**args)
        self.book.save()
        return account
