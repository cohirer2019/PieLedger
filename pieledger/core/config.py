# -*- coding:utf-8 -*-
import os
import sys

import yaml

try:
    config_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '../config.yml'))
    with open(config_path, 'r+') as ymlfile:
        ledger_config = yaml.load(ymlfile)
except IOError:
    print('Failed to locate config.yml')
    sys.exit(1)
