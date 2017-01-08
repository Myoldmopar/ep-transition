#!/usr/bin/env python

import sys
import unittest

valid_args = ['test', 'usage']


def usage():
    print("Usage: call with one of the following arguments:")
    for arg in valid_args:
        print("  " + sys.argv[0] + " " + arg)


def drive(argv):
    if len(argv) != 2:
        print("Error: Must call with 1 command line argument!")
        usage()
        return 1
    elif argv[1] == valid_args[0]:
        tests = unittest.TestLoader().discover('test')
        unittest.TextTestRunner().run(tests)
        return 0
    elif argv[1] == valid_args[1]:
        usage()
        return 0
    else:
        print("Error: Invalid command line argument passed in!")
        usage()
        return 1


if __name__ == "__main__":
    sys.exit(drive(sys.argv))
