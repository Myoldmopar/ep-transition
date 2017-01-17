#!/usr/bin/env python

import sys

from eptransition.manager import TransitionManager


import argparse

# available_versions = [8.5, 8.6, 8.7]
# parser = argparse.ArgumentParser(description='Transition an EnergyPlus Input File')
# parser.add_argument('original_input',
#                     action='store',
#                     nargs=1,
#                     required=True,
#                     help="The original input file to transition")
# parser.add_argument('original_version',
#                     action='store',
#                     nargs=1,
#                     choices=available_versions[:-1],
#                     required=True,
#                     help="The original version of the idf to transition from")
# parser.add_argument('integers', metavar='N', type=int, nargs='+',
#                     help='an integer for the accumulator')
#

class Argument:
    """
    Internal class used for establishing the possible action command line arguments for this tool
    """
    def __init__(self, cli_argument, num_additional_args, usage_hint):
        self.cli_argument = cli_argument
        self.num_additional_args = num_additional_args
        self.usage_hint = usage_hint


VALID_ARGS = [
    Argument('usage', 0, ''),
    Argument('update', 4,
             '<path/original/idf> <path/new/idf> <path/original/idd> <path/new/idd>')
]


def usage(test_mode=False):
    """
    Simple usage output for showing users how to call the program

    :param bool test_mode: This only shows output during !test_mode to avoid clogging up the test output
    """
    if not test_mode:  # pragma: no cover
        print("Usage: call with one of the following arguments:")
        for arg in VALID_ARGS:
            print("  " + sys.argv[0] + " " + arg.cli_argument + " " + arg.usage_hint)


def drive(argv, test_mode=False):
    """
    This is the highest level driving function for the transition process.  This interprets a list of arguments that
    mimic sys.argv.  (So that sys.argv can be passed in directly from other wrappers).  Allowed arguments are defined
    in the VALID_ARGS variable list.

    :param argv: An array of arguments, mimicking sys.argv.  As such, item 0 must be a dummy program name, followed
                 by real arguments.
    :param bool test_mode: A flag to decide whether to write to stdout or not
    :return: 0 for success, 1 for failure
    """
    # validate the argument list
    if len(argv) <= 1:
        if not test_mode:  # pragma: no cover
            print("Error: Must call with at least one command line argument!")
        usage(test_mode)
        return 1
    valid_keys = [a.cli_argument for a in VALID_ARGS]
    if argv[1] not in valid_keys:
        if not test_mode:  # pragma: no cover
            print("Error: Invalid command line argument passed in!")
            usage()
        return 1
    cur_arg = next(a for a in VALID_ARGS if a.cli_argument == argv[1])
    expected_total_argv = 2 + cur_arg.num_additional_args
    if len(argv) != expected_total_argv:
        if not test_mode:  # pragma: no cover
            print("Error: Invalid number of command line arguments")
        usage(test_mode)
        return 1
    # now do operations
    if argv[1] == VALID_ARGS[0].cli_argument:  # usage
        if not test_mode:  # pragma: no cover
            usage()
    elif argv[1] == VALID_ARGS[1].cli_argument:  # update
        manager = TransitionManager(argv[2], argv[3], argv[4], argv[5])
        manager.perform_transition()
    return 0


def main():  # pragma no cover
    """
    This function allows the transition tool to be called from the command line.  This function packages up sys.argv
    and passes them to the main drive function.  This function is exposed during installation via pip as the main
    entry point to the transition tool, callable directly from command line as: eptransition ...
    :return: Calls sys.exit upon completion with the return value from drive(), so 0 for success, 1 for failure.
    """
    sys.exit(drive(sys.argv))
