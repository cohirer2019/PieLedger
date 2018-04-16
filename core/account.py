# -*- coding:utf-8 -*-
from piecash.core import Account

from .base import BaseManager


class AccountManager(BaseManager):

    def find_by_guid(self, guid):
        return self.book.query(Account).get(guid)

    def find_by_parent(self, parent_guid, name, _type):
        return self.book.query(Account).filter(
            Account.parent_guid == parent_guid,
            Account.name == name,
            Account.type == _type).first()

    def create_account(self, **kw):
        kw['commodity'] = self.book.commodities.get(mnemonic="EUR")
        parent_guid = kw.pop('parent_guid', None)
        if parent_guid:
            kw['parent'] = self.find_by_guid(parent_guid)
            if not kw['parent']:
                raise ValueError('Parent account<%s> not found' % parent_guid)
        account = Account(**kw)
        self.book.save()
        return account
