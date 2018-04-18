# -*- coding:utf-8 -*-

def _patch_account():  #noqa

    import warnings
    from decimal import Decimal

    from sqlalchemy import Column, Float, inspect, exc as sa_exc
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

    def _sa_get_balance(self, recurse=True, commodity=None, as_decimal=False):
        """SQLAlchemy for calculating the splits and caching"""

        assert self.type != 'ROOT', \
            'Recurse only supported for non-root account'

        if commodity is None:
            commodity = self.commodity

        if self._cached_balance is not None:
            balance = self._cached_balance
        elif inspect(self).persistent:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", category=sa_exc.SAWarning)
                balance = (self.commodity.book.query(
                    func.sum(Split.quantity)
                ).filter(
                    Split.account_guid == self.guid
                ).scalar() or 0) * self.sign
            self._cached_balance = balance
        else:
            balance = 0

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

        if as_decimal:
            q = Decimal(1) / commodity.fraction
            balance = Decimal(balance).quantize(q)

        return balance

    Account.validate = _sa_validate
    Account.get_balance = _sa_get_balance
    Account._cached_balance = Column(
        'cached_balance', Float(as_decimal=True))


def _patch_split():

    from sqlalchemy import Column, Float
    from piecash.sa_extra import _DateTime
    from piecash.core import Split

    Split.running_total = Column(Float(as_decimal=True))
    Split.enter_date = Column(_DateTime, index=True)


def _patch_get_engine():

    from sqlalchemy import event, create_engine as sa_create_engine
    from piecash.core import session

    def _create_piecash_engine(uri_conn, **kw):
        connect_args = kw.pop('connect_args', {})
        if uri_conn.startswith('sqlite:'):
            # Turn off thread check
            connect_args['check_same_thread'] = False
        else:
            kw['isolation_level'] = 'READ COMMITTED'

        engine = sa_create_engine(uri_conn, connect_args=connect_args, **kw)
        if engine.name == 'sqlite':
            @event.listens_for(engine, "connect")
            def do_connect(dbapi_connection, connection_record):
                # disable pysqlite's emitting of the BEGIN statement entirely.
                # also stops it from emitting COMMIT before any DDL.
                dbapi_connection.isolation_level = None

            @event.listens_for(engine, "begin")
            def do_begin(conn):
                # emit our own BEGIN
                conn.execute("BEGIN")
        return engine

    session.create_piecash_engine = _create_piecash_engine


def _reg_invalidate_balance():

    from sqlalchemy import event
    from piecash.core import Split, Account
    from piecash.sa_extra import Session

    def _invalidate_balance(session, context, _):
        accounts = set()
        for obj in session.new:
            if not isinstance(obj, Split):
                continue
            # Caculate running total for the split and log it as cached balance
            acc = obj.account
            if acc not in accounts:
                accounts.add(acc)
                acc._cached_balance = None
                # Lock the account for running total calculation
                session.query(Account._cached_balance).filter(
                    Account.guid == acc.guid).with_for_update().scalar()
            acc._cached_balance = obj.running_total = \
                acc.get_balance(as_decimal=True, recurse=False) + obj.quantity

    event.listen(Session, 'before_flush', _invalidate_balance)


def patch_piecash():
    _patch_get_engine()
    _patch_account()
    _patch_split()
    _reg_invalidate_balance()
