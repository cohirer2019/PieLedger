# -*- coding:utf-8 -*-
import sys
import os
import warnings

import nose
import yaml

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

from pieledger.core.config import ledger_config  # noqa
from pieledger.core.book import create_book  # noqa


def _load_test_config():
    try:
        config_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), 'config.yml'))
        with open(config_path, 'r+') as ymlfile:
            test_config = yaml.load(ymlfile)
            if test_config:
                ledger_config.update(test_config)
    except IOError:
        warnings.warn('Failed to locate config.yml for testing')


class LedgerInitializer(nose.plugins.Plugin):

    def __init__(self, *args):
        super(LedgerInitializer, self).__init__(*args)
        self.enabled = True

    def options(self, parser, env):
        parser.add_option(
            '-S', '--sqlite', action='store_true', default=False,
            dest='sqlite', help='Use sqlite db')

    def configure(self, options, conf):
        self.sqlite = options.sqlite

    def begin(self):
        _load_test_config()
        if self.sqlite:
            ledger_config['db_uri'] = 'sqlite:///.sqlite'
        create_book(overwrite=True)


if __name__ == '__main__':
    additional_args = [
        '--rednose', '--nocapture', '--hide-skips', '--verbosity=2']
    nose.main(
        argv=sys.argv.extend(additional_args),
        addplugins=[LedgerInitializer()]
    )
