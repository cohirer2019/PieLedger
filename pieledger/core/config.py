# -*- coding:utf-8 -*-
import os
import sys

import yaml


config_path = os.environ.get('PIELEDGER_CONFIG')
if not config_path:
    config_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '../config.yml'))

try:
    with open(config_path, 'r+') as ymlfile:
        ledger_config = yaml.load(ymlfile)
except IOError:
    print('Failed to locate config.yml')
    sys.exit(1)
