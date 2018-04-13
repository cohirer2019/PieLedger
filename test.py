# -*- coding:utf-8 -*-
import sys
import argparse
import warnings
from unittest import main

import yaml

from core.config import ledger_config
from core.book import create_book
from tests import * #noqa


def _load_test_config():
    try:
        with open("config_test.yml", 'r+') as ymlfile:
            ledger_config.update(yaml.load(ymlfile))
    except IOError:
        warnings.warn('Failed to locate config_test.yml')


def _init_test(sqlite=False, **kw):
    _load_test_config()
    if sqlite:
        ledger_config['db_uri'] = 'sqlite:///.sqlite'
    create_book(overwrite=True)


if __name__ == '__main__':
    # Add additional arguments
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--sqlite', '-s', default=False, action='store_true')
    init_args, test_args = parser.parse_known_args()

    class MyUnitTest(main):
        USAGE = main.USAGE.replace(
            'Options:', 'Options:\n  -s, --sqlite     Use sqlite db')

        def runTests(self):
            _init_test(**vars(init_args))
            super(MyUnitTest, self).runTests()

    MyUnitTest(verbosity=3, argv=[sys.argv[0]] + test_args)
