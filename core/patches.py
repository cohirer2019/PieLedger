# -*- coding:utf-8 -*-

def _patch_account():  #noqa

    import warnings
    from sqlalchemy import Column, BIGINT, exc as sa_exc
    from sqlalchemy.sql import func
    from piecash.core import Account, Split
    from piecash.core.account import ACCOUNT_TYPES, \
        _is_parent_child_types_consistent, root_types, GncConversionError

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

    def _sa_get_balance(self, recurse=True, commodity=None, force=False):
        """SQLAlchemy for calculating the splits and caching"""

        assert self.type != 'ROOT', \
            'Recurse only supported for non-root account'

        if commodity is None:
            commodity = self.commodity

        if self._cached_balance is not None:
            balance = self._cached_balance
        else:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", category=sa_exc.SAWarning)
                balance = (self.commodity.book.query(
                    func.sum(Split.quantity)
                ).filter(
                    Split.account_guid == self.guid
                ).scalar() or 0) * self.sign
            self._cached_balance = balance

        if commodity != self.commodity:
            try:
                factor = self.commodity.currency_conversion(commodity)
                balance = balance * factor
            except GncConversionError:
                factor1 = self.commodity.currency_conversion(
                    self.parent.commodity)
                factor2 = self.parent.commodity.currency_conversion(commodity)
                factor = factor1 * factor2
                balance = balance * factor

        if recurse and self.children:
            balance += sum(acc.get_balance(
                recurse=recurse, commodity=commodity) for acc in self.children)

        return balance

    Account.validate = _sa_validate
    Account.get_balance = _sa_get_balance
    Account._cached_balance = Column('cached_balance', BIGINT())


def _reg_invalidate_balance():
    from sqlalchemy import event
    from piecash.core import Split
    from piecash.sa_extra import Session

    def _invalidate_balance(session, context, _):
        for obj in session.new:
            if isinstance(obj, Split):
                obj.account._cached_balance = None

    event.listen(Session, 'before_flush', _invalidate_balance)


def patch_piecash():
    _patch_account()
    _reg_invalidate_balance()
