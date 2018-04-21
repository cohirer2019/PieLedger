# -*- coding:utf-8 -*-
import unittest
from contextlib import contextmanager
from functools import wraps

import six
from sqlalchemy import event, inspect
from piecash.core import Account, Transaction, Split, \
    session as piecash_session
from piecash.core.session import adapt_session as _adapt_session, \
    create_piecash_engine as _create_engine

from core.book import open_book


def adapt_session(session, book, readonly):
    session.begin_nested()

    @event.listens_for(session, "after_transaction_end")
    def restart_savepoint(session, transaction):
        if transaction.nested and not transaction._parent.nested:
            session.expire_all()
            session.begin_nested()

    _adapt_session(session, book, readonly)


@contextmanager
def _test_context(conn):
    trans = conn.begin()
    try:
        yield
    finally:
        trans.rollback()


@contextmanager
def _real_context():
    _tmp_adapt_session = piecash_session.adapt_session
    _tmp_piecash_engine = piecash_session.create_piecash_engine
    piecash_session.adapt_session = _adapt_session
    piecash_session.create_piecash_engine = _create_engine
    try:
        yield
    finally:
        piecash_session.adapt_session = _tmp_adapt_session
        piecash_session.create_piecash_engine = _tmp_piecash_engine


def book_context(*args, **kw):
    join_session = kw.get('join_session', True)

    def decorator(func):
        @wraps(func)
        def func_wraper(self, *a, **ka):
            if not join_session:
                # Order matters
                with _real_context(), open_book() as book:
                    return func(self, book, *a, **ka)
            with open_book() as book, _test_context(book.session.get_bind()):
                return func(self, book, *a, **ka)
        return func_wraper

    if args and callable(args[0]):
        return decorator(args[0])
    return decorator


class BaseTestCase(unittest.TestCase):

    @classmethod
    def create_piecash_engine(cls, uri_conn, **kw):
        """Setup to allow revert any db changes after test"""
        if not hasattr(cls, '_connection'):
            engine = _create_engine(uri_conn, **kw)
            cls._connection = engine.connect()
            cls._connection.url = uri_conn
            cls._root_trans = cls._connection.begin()
        return cls._connection

    @classmethod
    def setUpClass(cls):
        piecash_session.create_piecash_engine = cls.create_piecash_engine
        piecash_session.adapt_session = adapt_session

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, '_connection'):
            cls._root_trans.rollback()
            cls._connection.close()

        # Restore the original
        piecash_session.adapt_session = _adapt_session
        piecash_session.create_piecash_engine = _create_engine

    @staticmethod
    def make_account(book, name, _type, commodity=None, parent=None, **kw):
        if not commodity:
            commodity = book.default_currency
        if not parent:
            parent = book.root_account
        return Account(name, _type, commodity=commodity, parent=parent, **kw)

    @staticmethod
    def transfer(from_acc, to_acc, value, enter_date=None):
        currency = from_acc.commodity
        assert currency == to_acc.commodity, \
            'Commodities of accounts should be the same'
        nvalue = '-%s' % value if isinstance(value, str) else -value
        trans = Transaction(currency=currency, splits=[
            Split(account=from_acc, value=nvalue),
            Split(account=to_acc, value=value),
        ])
        if enter_date:
            enter_date = enter_date.replace(microsecond=0)
            for e in (trans, trans.splits[0], trans.splits[1]):
                e.enter_date = enter_date
        return trans

    @book_context(join_session=False)
    def _delete(self, book, *args):
        for o in args:
            o = book.session.merge(o)
            if not inspect(o).key:
                continue
            book.delete(o)
        book.save()

    def deleteAfter(self, *args):
        self.addCleanup(self._delete, *args)

    def assertCountEqual(self, *args):
        if six.PY2:
            return six.assertCountEqual(self, *args)
        super(BaseTestCase, self).assertCountEqual(*args)
