# -*- coding:utf-8 -*-
import sys

import yaml

try:
    with open("config.yml", 'r+') as ymlfile:
        ledger_config = yaml.load(ymlfile)
except IOError:
    print('Failed to locate config.yml')
    sys.exit(1)
