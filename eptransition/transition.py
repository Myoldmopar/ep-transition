#!/usr/bin/env python

import argparse
import logging
import sys

from eptransition import __name__ as logname
from eptransition import __version__, __description__
from eptransition.manager import TransitionManager
from eptransition.versions.versions import TRANSITIONS


def main(args=None):
    """
    This is the highest level driving function for the transition process.  This interprets either sys.argv directly,
    or a list of arguments that mimic sys.argv.  (So that sys.argv can be passed in directly from other wrappers).
    This function is called from the command line via the pip installation.

    :param args: An optional array of arguments, mimicking sys.argv.  As such, item 0 must be a dummy program name,
                 followed by real arguments.  If this is not passed in, sys.argv is assumed.
    :return: 0 on success, 1 for failure
    :raises Exception: If the --raise flag is used, it will raise the underlying Exception at the first failure
    """

    # set up the highest level logger
    logger = logging.getLogger("eptransition")
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler("{}.log".format(logname))
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
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
    parser.add_argument("input_files", help="The original input files to transition", nargs="+")
    parser.add_argument("-v", "--version", action="version", version="%(prog)s {version}".format(version=__version__))
    parser.add_argument("-r", "--raise", dest="throw", action="store_const",
                        const=True, default=False,
                        help="With this flag, the transition will stop at the first failure and raise an exception;"
                        " if the flag is not passed in, the transition will continue through all requested transitions"
                        " and return a 0 or 1 without raising an exception.  (default: Do not raise)")
    parser.add_argument("-V", "--verbose", dest="verbose", action="store_const",
                        const=True, default=False,
                        help="Turns on louder output to stdout, full detail still in the log file (default: quiet)")
    args = parser.parse_args(args=args)
    if args.verbose:  # pragma no cover -- I don't want this output during tests
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    logger.debug("***Transition started: attempting to transition {} files".format(len(args.input_files)))
    failed_files = []
    for input_file in args.input_files:
        try:
            manager = TransitionManager(input_file)
            manager.perform_transition()
        except Exception as e:
            logger.exception(
                "Problem occurred during transition, skipping this file!\n File: {}\n Message: {}".format(
                    input_file, str(e)))
            failed_files.append(input_file)
            if args.throw:
                raise

    for ff in failed_files:  # pragma no cover -- I don't want output during tests, raise exception instead
        print(" ** Failed to transition: {}".format(ff))

    # if successful, return 0
    if failed_files:  # pragma no cover -- I don't want to print stdout during tests, so exceptions are raised instead
        return 1
    else:
        return 0


if __name__ == "__main__":  # pragma no cover
    sys.exit(main())
