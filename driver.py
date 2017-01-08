#!/usr/bin/env python

import sys
import unittest

from transition.idf.processidf import IDFProcessor


class Argument:
    def __init__(self, cli_argument, additional_arg, usage_hint):
        self.cli_argument = cli_argument
        self.additional_arg = additional_arg
        self.usage_hint = usage_hint


valid_args = [Argument('test', False, ''),
              Argument('usage', False, ''),
              Argument('update', True, '<path/to/file/to/update>')]


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
    if cur_arg.additional_arg:
        expected_total_argv = 3
    else:
        expected_total_argv = 2
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
        input_file = argv[2]
        i = IDFProcessor()
        i.process_file_given_file_path(input_file)
    return 0


if __name__ == "__main__":
    sys.exit(drive(sys.argv))
