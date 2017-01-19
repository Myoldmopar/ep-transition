#!/usr/bin/env python

import argparse
import sys

from eptransition import __version__, __description__
from eptransition.exceptions import ManagerProcessingException, FileAccessException, FileTypeException
from eptransition.manager import TransitionManager
from eptransition.versions.versions import TRANSITIONS


def main(args=None):
    """
    This is the highest level driving function for the transition process.  This interprets either sys.argv directly,
    or a list of arguments that mimic sys.argv.  (So that sys.argv can be passed in directly from other wrappers).
    This function is called from the command line via the pip installation.

    :param args: An optional array of arguments, mimicking sys.argv.  As such, item 0 must be a dummy program name,
                 followed by real arguments.  If this is not passed in, sys.argv is assumed.
    :return: 0 for success, 1 for failure
    """
    if args is None:  # pragma no cover
        args = sys.argv[1:]
    epilogue = "This version of the E+ translator includes the following translations:\n"
    for k, v in TRANSITIONS.items():
        if v.transitions:
            epilogue += " * {} to {}  --  ({} transitions)\n".format(v.start_version, v.end_version, len(v.transitions))
    parser = argparse.ArgumentParser(description=__description__, epilog=epilogue,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("original_input", help="The original input file to transition", nargs=1)
    parser.add_argument("-o", "--output", action="store", help="Path to write the transitioned input file structure")
    parser.add_argument("-p", "--previdd", action="store", help="Path to an original IDD")
    parser.add_argument("-n", "--newidd", action="store", help="Path to a new IDD")
    parser.add_argument("-v", "--version", action='version', version='%(prog)s {version}'.format(version=__version__))
    args = parser.parse_args(args=args)
    try:
        manager = TransitionManager(args.original_input[0], args.output, args.previdd, args.newidd)
    except Exception as e:  # pragma no cover
        print("Could not instantiate manager from command line args...exception message follows\n{}".format(e.message))
        return 1
    try:
        manager.perform_transition()
    except (FileAccessException, FileTypeException, ManagerProcessingException) as e:  # pragma no cover
        print("Problem occurred during transition! Exception message: \n " + str(e))
        return 1
    return 0


if __name__ == "__main__":  # pragma no cover
    sys.exit(main())
