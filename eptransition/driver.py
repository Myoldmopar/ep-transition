#!/usr/bin/env python

import sys
import unittest

from manager import TransitionManager


class Argument:
    def __init__(self, cli_argument, num_additional_args, usage_hint):
        self.cli_argument = cli_argument
        self.num_additional_args = num_additional_args
        self.usage_hint = usage_hint


valid_args = [
    Argument('test', 0, ''),
    Argument('usage', 0, ''),
    Argument('update', 4, '<path/to/original/idf> <path/to/new/idf> <path/to/original/idd> <path/to/new/idd>')
]


def usage(test_mode=False):
    if not test_mode:  # pragma: no cover
        print("Usage: call with one of the following arguments:")
        for arg in valid_args:
            print("  " + sys.argv[0] + " " + arg.cli_argument + " " + arg.usage_hint)


def drive(argv, test_mode=False):
    # validate the argument list
    if len(argv) <= 1:
        if not test_mode:  # pragma: no cover
            print("Error: Must call with at least one command line argument!")
        usage(test_mode)
        return 1
    valid_keys = [a.cli_argument for a in valid_args]
    if argv[1] not in valid_keys:
        if not test_mode:  # pragma: no cover
            print("Error: Invalid command line argument passed in!")
            usage()
        return 1
    cur_arg = next((a for a in valid_args if a.cli_argument == argv[1]), None)
    if not cur_arg:  # pragma: no cover
        if not test_mode:
            print("Error: Unexpected error in processing command line arguments")
        usage(test_mode)
        return 1
    expected_total_argv = 2 + cur_arg.num_additional_args
    if len(argv) != expected_total_argv:
        if not test_mode:  # pragma: no cover
            print("Error: Invalid number of command line arguments")
        usage(test_mode)
        return 1
    # now do operations
    if argv[1] == valid_args[0].cli_argument:  # test
        tests = unittest.TestLoader().discover('test')
        unittest.TextTestRunner().run(tests)
    elif argv[1] == valid_args[1].cli_argument:  # usage
        if not test_mode:  # pragma: no cover
            usage()
    elif argv[1] == valid_args[2].cli_argument:  # update
        manager = TransitionManager(argv[2], argv[3], argv[4], argv[5])
        manager.perform_transition()
    return 0


def drive_from_cmdline():  # pragma no cover
    sys.exit(drive(sys.argv))


if __name__ == "__main__":  # pragma no cover
    drive_from_cmdline()
