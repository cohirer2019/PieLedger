# -*- coding:utf-8 -*-


def _patch_hybird_property(hybrid_property, num_col, denom_col):
    from decimal import Decimal

    num_name, denom_name = \
        "_{}".format(num_col.name), "_{}".format(denom_col.name)
    name = num_col.name.split("_")[0]

    def _expr(cls):
        # No cast required for mysql
        return (num_col / denom_col).label(name)

    def _fget(self):
        # The method with piecash lose the info of denom and we return it
        # with the new method here
        num, denom = getattr(self, num_name), getattr(self, denom_name)
        if num is not None:
            return Decimal(1) / denom * num

    return hybrid_property.overrides.expression(_expr).overrides.getter(_fget)


def _hybird_property(num_col, denom_col):
    from piecash._common import hybrid_property_gncnumeric
    p = hybrid_property_gncnumeric(num_col, denom_col)
    return _patch_hybird_property(p, num_col, denom_col)


def _patch_account():  #noqa

    from sqlalchemy import Column, BIGINT, inspect
    from sqlalchemy.sql import func
    from piecash.core import Account, Split
    from piecash.core.account import ACCOUNT_TYPES, \
        _is_parent_child_types_consistent, root_types, GncConversionError
    from core.utils import currency_decimal

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

    def _sa_get_balance(self, recurse=True, commodity=None):
        """SQLAlchemy for calculating the splits and caching"""

        assert self.type != 'ROOT', \
            'Recurse only supported for non-root account'

        if commodity is None:
            commodity = self.commodity

        if self._cached_balance is not None:
            balance = self._cached_balance
        elif inspect(self).persistent:
            balance = (self.commodity.book.query(
                func.sum(Split.quantity)
            ).filter(
                Split.account_guid == self.guid
            ).scalar() or 0) * self.sign
            # Cast to decimal with commodity fraction
            balance = currency_decimal(balance, self.commodity)
            self._cached_balance = balance
        else:
            balance = currency_decimal(0, self.commodity)

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

    Account._cached_balance_num = balance_num = Column(
        'cached_balance_num', BIGINT())
    Account._cached_balance_denom = balance_denom = Column(
        'cached_balance_denom', BIGINT())
    Account._cached_balance = _hybird_property(balance_num, balance_denom)


def _patch_split():

    from datetime import datetime
    from sqlalchemy import Column, BIGINT
    from piecash.sa_extra import _DateTime
    from piecash.core import Split

    Split._running_balance_num = balance_num = Column(
        'running_balance_num', BIGINT(), nullable=False)
    Split._running_balance_denom = balance_denom = Column(
        'running_balance_denom', BIGINT(), nullable=False)
    Split.running_balance = _hybird_property(balance_num, balance_denom)

    Split.quantity = _patch_hybird_property(
        Split.quantity, Split._quantity_num, Split._quantity_denom)
    Split.value = _patch_hybird_property(
        Split.value, Split._value_num, Split._value_denom)

    Split.enter_date = Column(
        _DateTime, index=True,
        default=lambda: datetime.now().replace(microsecond=0))


def _patch_get_engine():

    from sqlalchemy import event, create_engine as sa_create_engine
    from piecash.core import session

    def _sign(val):
        if val:
            return 1 if val > 0 else -1
        else:
            return val

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
                # Custom sign function
                dbapi_connection.create_function("sign", 1, _sign)

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
                # Lock the account for balance calculation
                session.query(Account._cached_balance).filter(
                    Account.guid == acc.guid
                ).with_for_update().scalar()
            # Add up the balance with splits in the sessio
            acc._cached_balance = obj.running_balance = \
                acc.get_balance(recurse=False) + obj.quantity * acc.sign

    event.listen(Session, 'before_flush', _invalidate_balance)


def patch_piecash():
    _patch_get_engine()
    _patch_account()
    _patch_split()
    _reg_invalidate_balance()
