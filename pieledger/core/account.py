# -*- coding:utf-8 -*-
from piecash.core import Account

from .base import BaseManager


class AccountManager(BaseManager):

    model = Account

    def find_by_parent(
            self, parent_guid, name, _type, placeholder, lock_parent=False):
        if not parent_guid and placeholder:
            parent_guid = self.book.root_account_guid
        if lock_parent:
            self.book.query(Account).with_for_update().get(parent_guid)

        return self.book.query(Account).filter(
            Account.parent_guid == parent_guid,
            Account.name == name,
            Account.type == _type).first()

    def create(self, currency=None, **kw):
        kw['commodity'] = self.book.currencies.get(mnemonic=currency) \
            if currency else self.book.default_currency
        parent_guid = kw.pop('parent_guid', None)
        if parent_guid:
            kw['parent'] = self.find_by_guid(parent_guid)
            if not kw['parent']:
                raise ValueError('Parent account<%s> not found' % parent_guid)
        elif kw.get('placeholder'):
            kw['parent'] = self.book.root_account
        account = Account(**kw)
        return account
