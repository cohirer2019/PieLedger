# -*- coding:utf-8 -*-
import os
import sys

import yaml


config_path = os.environ.get('PIELEDGER_CONFIG')
if not config_path:
    config_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '../config.yml'))
if not os.path.isfile(config_path):
    config_path = 'config.yml'  # Fallback to cwd

try:
    with open(config_path) as ymlfile:
        ledger_config = yaml.load(ymlfile)
except IOError:
    print('Failed to locate config.yml')
    sys.exit(1)
