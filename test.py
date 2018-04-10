# -*- coding:utf-8 -*-
import sys
from unittest import main
import argparse

from tests import * #noqa
from tests.base import init_test


if __name__ == '__main__':
    # Add additional arguments
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--sqlite', '-s', default=False, action='store_true')
    main.USAGE = main.USAGE.replace(
        'Options:', 'Options:\n  -s, --sqlite     Use sqlite memory db')

    init_args, test_args = parser.parse_known_args()
    init_test(**vars(init_args))
    main(verbosity=2, argv=[sys.argv[0]] + test_args)
