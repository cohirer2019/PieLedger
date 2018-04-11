# -*- coding:utf-8 -*-
import sys
import argparse
from unittest import main

from tests import * #noqa
from tests.base import init_test


if __name__ == '__main__':
    # Add additional arguments
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--sqlite', '-s', default=False, action='store_true')
    init_args, test_args = parser.parse_known_args()

    class MyUnitTest(main):
        USAGE = main.USAGE.replace(
            'Options:', 'Options:\n  -s, --sqlite     Use sqlite db')

        def runTests(self):
            init_test(**vars(init_args))
            super(MyUnitTest, self).runTests()

    MyUnitTest(verbosity=2, argv=[sys.argv[0]] + test_args)
