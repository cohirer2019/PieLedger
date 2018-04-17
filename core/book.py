# -*- coding:utf-8 -*-
import warnings

import piecash
from piecash.core import Account, Transaction
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
                ('ix_transactions_enter_date', Transaction.enter_date)):
            schema.Index(key, column).create(bind=engine)


def open_book(readonly=False):
    return piecash.open_book(
        uri_conn=_db_uri(), open_if_lock=True, do_backup=False,
        readonly=readonly)
