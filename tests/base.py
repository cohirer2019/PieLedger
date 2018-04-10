# -*- coding:utf-8 -*-
import sys
import unittest
import warnings

import yaml

from core.config import ledger_config
from core.book import create_book


def _load_test_config():
    try:
        with open("config_test.yml", 'r+') as ymlfile:
            ledger_config.update(yaml.load(ymlfile))
    except IOError:
        warnings.warn('Failed to locate config_test.yml')


def init_test(sqlite=False, **kw):
    _load_test_config()
    if sqlite:
        ledger_config['db_uri'] = 'sqlite://'
    create_book(overwrite=True)
