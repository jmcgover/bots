#! /usr/bin/env python3

import os
import sys
import errno

import argparse

# Logging
import logging
from logging import handlers
LOGGER = logging.getLogger(__name__)
SH = logging.StreamHandler()
FH = logging.handlers.RotatingFileHandler("log.log", maxBytes=5 * 1000000, backupCount = 5)
SH.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(message)s"))
FH.setFormatter(logging.Formatter("%(asctime)s:%(lineno)s:%(funcName)s:%(levelname)s:%(message)s"))
LOGGER.setLevel(logging.DEBUG)
LOGGER.addHandler(SH)
LOGGER.addHandler(FH)

DEFAULT_FILENAME="MuellerReport.txt"
DESCRIPTION = """Parses the MuellerReport file into the appropriate data structures to enable text generation."""
def get_arg_parser():
    parser = argparse.ArgumentParser(prog=sys.argv[0], description=DESCRIPTION)
    parser.add_argument("-f", "--filename",
            help = "file to parse (default is %s)" % DEFAULT_FILENAME)
    parser.add_argument("-i", "--info",
            help = "set console logging output to INFO")
    parser.add_argument("-d", "--debug",
            help = "set console logging output to DEBUG")
    parser.set_defaults(
            filename = DEFAULT_FILENAME
            )
    return parser


def main():
    parser = get_arg_parser()
    args = parser.parse_args()

    # Logging Information
    if args.info:
        SH.setLevel(logging.INFO)
    if args.debug:
        SH.setLevel(logging.DEBUG)

    # Open File
    LOGGER.info("Opening file at %s", args.filename)
    doc_text = None
    try:
        with open(args.filename, 'r') as file:
            LOGGER.info("Opened %s" % args.filename)
            doc_text = file.read()
    except IOError as e:
        LOGGER.error("Failed to open %s: %s" % (args.filename, e))
        return e.errno

    return 0

if __name__ == "__main__":
    rtn = main()
    sys.exit(rtn)
