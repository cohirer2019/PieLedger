# -*- coding:utf-8 -*-
import piecash

from .config import ledger_config


db_uri = ledger_config.get('db_uri')
assert db_uri, 'PieLedger requires GnuCash work with database and '\
    'should have db_uri defined'


def create_book(overwrite=False):
    piecash.create_book(
        keep_foreign_keys=True,
        uri_conn=db_uri,
        overwrite=overwrite
    )


def open_book(read_only=False):
    return piecash.open_book(
        uri_conn=db_uri, open_if_lock=True, read_only=read_only)
