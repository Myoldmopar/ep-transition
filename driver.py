#!/usr/bin/env python

import sys
import os
import shutil
import subprocess
import unittest

valid_args = ['test', 'usage']


def usage():
    print("Usage: call with one of the following arguments:")
    for arg in valid_args:
        print("  " + sys.argv[0] + " " + arg)

if len(sys.argv) != 2:
    print("Error: Must call with 1 command line argument!")
    usage()
    sys.exit(1)
elif sys.argv[1] == valid_args[0]:
    tests = unittest.TestLoader().discover('test')
    unittest.TextTestRunner().run(tests)
    sys.exit(0)
elif sys.argv[1] == valid_args[1]:
    usage()
    sys.exit(0)
else:
    print("Error: Invalid command line argument passed in!")
    usage()
    sys.exit(1)

