# -*- coding:utf-8 -*-
import sys
import warnings

import nose
import yaml

from core.config import ledger_config
from core.book import create_book


def _load_test_config():
    try:
        with open('config_test.yml', 'r+') as ymlfile:
            ledger_config.update(yaml.load(ymlfile))
    except IOError:
        warnings.warn('Failed to locate config_test.yml')


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
        '--rednose', '--nocapture', '--verbosity=2']
    nose.main(
        module='tests', argv=sys.argv.extend(additional_args),
        addplugins=[LedgerInitializer()]
    )
