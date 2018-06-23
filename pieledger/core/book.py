# -*- coding:utf-8 -*-
import warnings
import backoff
from functools import wraps

import piecash
from piecash.core import Account, Transaction, Split
from sqlalchemy import schema

from .config import ledger_config


def _db_uri():
    db_uri = ledger_config.get('db_uri')
    assert db_uri, 'PieLedger requires GnuCash work with database and '\
        'should have db_uri defined'
    return db_uri


def _create_book(overwrite=False, **kw):
    return piecash.create_book(
        keep_foreign_keys=True, uri_conn=_db_uri(), overwrite=overwrite)


def create_book(**kw):
    with warnings.catch_warnings(), _create_book(**kw) as book:
        # Ignore warning for mysql index prefix too long
        warnings.simplefilter("ignore")
        # Add additional indexes used by pieledger
        engine = book.session.get_bind()
        for key, column in (
                ('ix_account_name', Account.name),
                ('ix_transactions_enter_date', Transaction.enter_date),
                ('ix_split_action', Split.action)):
            schema.Index(key, column).create(bind=engine)


def open_book(readonly=False):
    return piecash.open_book(
        uri_conn=_db_uri(), open_if_lock=True, do_backup=False,
        readonly=readonly)


def book_context(*args, **kw):
    def decorator(func):
        @wraps(func)
        def func_wraper(self, *a, **ka):
            with open_book() as book:
                try:
                    return func(self, book, *a, **ka)
                except Exception:
                    book.cancel()
                    raise
        if 'retry_for' in kw:
            options = {
                'jitter': backoff.full_jitter,
                'interval': 0.2,
                'max_tries': 3
            }
            options.update(kw.get('retry_options', {}))
            return backoff.on_exception(
                options.pop('wait_gen', backoff.constant),
                kw['retry_for'], **options)(func_wraper)
        return func_wraper

    if args and callable(args[0]):
        return decorator(args[0])
    return decorator
