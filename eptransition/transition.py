#!/usr/bin/env python

import argparse
import sys
import logging

from eptransition import __version__, __description__
from eptransition.exceptions import ManagerProcessingException, FileAccessException, FileTypeException
from eptransition.manager import TransitionManager
from eptransition.versions.versions import TRANSITIONS
from eptransition import __name__ as logname


def main(args=None):
    """
    This is the highest level driving function for the transition process.  This interprets either sys.argv directly,
    or a list of arguments that mimic sys.argv.  (So that sys.argv can be passed in directly from other wrappers).
    This function is called from the command line via the pip installation.

    :param args: An optional array of arguments, mimicking sys.argv.  As such, item 0 must be a dummy program name,
                 followed by real arguments.  If this is not passed in, sys.argv is assumed.
    :return: 0 for success, 1 for failure
    """

    # set up the highest level logger
    logger = logging.getLogger('eptransition')
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('{}.log'.format(logname))
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    # now start processing
    if args is None:  # pragma no cover
        logger.debug("Call to main() with no function arguments; using sys.argv")
        args = sys.argv[1:]
    epilogue = "This version of the E+ translator includes the following translations:\n"
    for k, v in TRANSITIONS.items():
        if v.transitions:
            epilogue += " * {} to {}  --  ({} transitions)\n".format(v.start_version, v.end_version, len(v.transitions))
    parser = argparse.ArgumentParser(description=__description__, epilog=epilogue,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("input_files", help="The original input files to transition", nargs='+')
    parser.add_argument("-v", "--version", action='version', version='%(prog)s {version}'.format(version=__version__))
    args = parser.parse_args(args=args)
    logger.debug("***Transition started: attempting to transition {} files".format(len(args.input_files)))
    for input_file in args.input_files:
        try:
            manager = TransitionManager(input_file)
        except Exception as e:
            logger.exception(
                "Could not instantiate manager from command line args...exception message follows\n{}".format(e.message))
            raise
        try:
            manager.perform_transition()
        except (FileAccessException, FileTypeException, ManagerProcessingException) as e:
            logger.exception("Problem occurred during transition! Exception message: \n " + str(e))
            raise

    # if successful, return 0
    return 0


if __name__ == "__main__":  # pragma no cover
    sys.exit(main())
