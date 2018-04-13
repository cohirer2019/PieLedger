# -*- coding:utf-8 -*-
import unittest

from sqlalchemy import event, create_engine as sa_create_engine
from piecash.core import Account, Transaction, Split, \
    session as piecash_session
from piecash.core.session import adapt_session as _adapt_session
from piecash.sa_extra import create_piecash_engine as _create_engine

from core.book import open_book


def adapt_session(session, book, readonly):
    session.begin_nested()

    @event.listens_for(session, "after_transaction_end")
    def restart_savepoint(session, transaction):
        if transaction.nested and not transaction._parent.nested:
            session.expire_all()
            session.begin_nested()

    _adapt_session(session, book, readonly)


def _get_engine(uri_conn, **kw):
    connect_args = kw.pop('connect_args', {})
    if uri_conn.startswith('sqlite:'):
        # Turn off thread check
        connect_args['check_same_thread'] = False
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


class BaseTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        # Setup to allow revert any db changes after test
        def create_piecash_engine(uri_conn, **kw):
            if not hasattr(cls, '_connection'):
                engine = _get_engine(uri_conn, **kw)
                cls._connection = engine.connect()
                cls._connection.url = uri_conn
                cls._root_trans = cls._connection.begin()
            return cls._connection

        piecash_session.create_piecash_engine = create_piecash_engine
        piecash_session.adapt_session = adapt_session

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, '_connection'):
            cls._root_trans.rollback()
            cls._connection.close()

        # Restore the original
        piecash_session.adapt_session = _adapt_session
        piecash_session.create_piecash_engine = _create_engine

    def setUp(self):
        self.book = open_book()
        self._trans = self._connection.begin()

    def tearDown(self):
        self.book.close()
        self._trans.rollback()

    def make_account(self, name, _type, commodity=None, parent=None, **kw):
        if not commodity:
            commodity = self.book.default_currency
        if not parent:
            parent = self.book.root_account
        return Account(name, _type, commodity=commodity, parent=parent, **kw)

    @staticmethod
    def transfer(from_acc, to_acc, value):
        currency = from_acc.commodity
        assert currency == to_acc.commodity, \
            'Commodities of accounts should be the same'
        return Transaction(currency=currency, splits=[
            Split(account=from_acc, value=-value),
            Split(account=to_acc, value=value),
        ])
