# -*- coding:utf-8 -*-


def _patch_account():

    from piecash.core import Account
    from piecash.core.account import ACCOUNT_TYPES, \
        _is_parent_child_types_consistent, root_types

    def _sa_validate(self):
        if self.type not in ACCOUNT_TYPES:
            raise ValueError(
                'Account_type "{}" is not in {}'.format(
                    self.type, ACCOUNT_TYPES))

        if self.parent:
            if not _is_parent_child_types_consistent(
                    self.parent.type, self.type, self.book.control_mode):
                raise ValueError(
                    'Child type "{}" is not consistent with parent '
                    'type {}'.format(self.type, self.parent.type))

            for acc in self.book.query(Account).filter(
                    Account.parent_guid == self.parent_guid,
                    Account.name == self.name):
                if acc.name == self.name and acc.guid != self.guid:
                    raise ValueError(
                        '{} has two children with the same name {} : {} '
                        'and {}'.format(self.parent, self.name, self, acc))
        else:
            if self.type in root_types:
                if self.name not in ['Template Root', 'Root Account']:
                    raise ValueError(
                        '{} is a root account but has a name = "{}"'.format(
                            self, self.name))
            else:
                raise ValueError(
                    '{} has no parent but is not a root account'.format(self))

    Account.validate = _sa_validate


def patch_piecash():
    _patch_account()
