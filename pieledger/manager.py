# -*- coding:utf-8 -*-
import sys
import os

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

from pieledger.cli.base import manager  # noqa


if __name__ == '__main__':
    manager()
