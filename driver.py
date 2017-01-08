#!/usr/bin/env python

import sys
import unittest

valid_args = ['test', 'usage']


def usage(test_mode=False):
    if not test_mode:  # pragma: no cover
        print("Usage: call with one of the following arguments:")
        for arg in valid_args:
            print("  " + sys.argv[0] + " " + arg)


def drive(argv, test_mode=False):
    if len(argv) != 2:
        if not test_mode:  # pragma: no cover
            print("Error: Must call with 1 command line argument!")
        usage(test_mode)
        return 1
    elif argv[1] == valid_args[0]:
        tests = unittest.TestLoader().discover('test')
        unittest.TextTestRunner().run(tests)
        return 0
    elif argv[1] == valid_args[1]:
        if not test_mode:  # pragma: no cover
            usage()
        return 0
    else:
        if not test_mode:  # pragma: no cover
            print("Error: Invalid command line argument passed in!")
            usage()
        return 1


if __name__ == "__main__":
    sys.exit(drive(sys.argv))
