#! /usr/bin/env python3

import os
import sys
import errno

import argparse

import re
from pprint import pprint

import json

#from nltk.tokenize import sent_tokenize

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
DEFAULT_OUTPUT="cbdq.json"
DESCRIPTION = """Parses the MuellerReport file into the appropriate data structures to enable text generation."""
def get_arg_parser():
    parser = argparse.ArgumentParser(prog=sys.argv[0], description=DESCRIPTION)
    parser.add_argument("-f", "--filename",
            help = "file to parse (default is %s)" % DEFAULT_FILENAME)
    parser.add_argument("-o", "--output",
            help = "file to save the Cheap Bots Done Quick JSON to (default is %s)" % DEFAULT_OUTPUT)
    parser.add_argument("-i", "--info",
            help = "set console logging output to INFO")
    parser.add_argument("-d", "--debug",
            help = "set console logging output to DEBUG")
    parser.set_defaults(
            filename = DEFAULT_FILENAME,
            output = DEFAULT_OUTPUT
            )
    return parser

def ngrams(doc, n=2):
    return ngrams


def get_sents(doc):

    # Get the Harm To Whatever stuff as their own sentences
    capture_inbetween = re.sub(r"(?<!\.)\n{2,}", " ` ", doc)

    # Remove extra whitespace within
    doc_text = ' '.join(capture_inbetween.split())

    # Create a list of sentences
    sent_split = re.split("((?<!(v|[A-Z]|[0-9]))(?<!(Mr|Ms|MR|MS|Jr|jr|Dr|dr|No))(?<!Mrs)(?<!et al)(?<!(Jan|Feb|Mar|Apr|Jun|Jul|Aug|Oct|Nov|Dec|Doc))[.?!`])(\"?)", doc_text)
    #sent_split = sent_tokenize(doc_text)

    # Filter out the empty garbage items
    non_empty = [s.strip() for s in sent_split if s and len(s.strip()) > 0];

    print(non_empty)

    # Append the punctuation to the previous sentence
    punct_set = set(".?!")
    sents = []
    if not non_empty:
        return None
    sents.append(non_empty[0])
    for i in range(1,len(non_empty)):
        s = non_empty[i]
        assert(len(s) > 0)
        if s == "`":
            continue
        if s[0] in punct_set or s == '"':
            sents[-1] += s
            continue
        #s = s.replace("!","")
        sents.append(s)
    sents = [s.strip() for s in sents if len(s) > 3 or "bad" in s.lower()];
    #sents = [s.strip() for s in sents if len(s)];
    return sents

def cbdq_json_dict(sents):
    return {"origin" : sents}

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
    raw_doc = None
    try:
        with open(args.filename, 'r') as file:
            LOGGER.info("Opened %s" % args.filename)
            raw_doc = file.read()
    except IOError as e:
        LOGGER.error("Failed to open %s: %s" % (args.filename, e))
        return e.errno

    # Format Doc
    LOGGER.info("Formatting Document");
    sents = get_sents(raw_doc)
    num_too_long = 0
    for i,s in enumerate(sents):
        print("SENTENCE %d: '%s'" % (i, s))
        threshold = 6
        if len(s) == threshold:
            print("WARNING: Exactly %d characters (%d): %s" % (len(s), len(s), s))
            num_too_long += 1
        #if len(s) > 280:
        #    LOGGER.warning("Too many characters (%d): %s" % (len(s), s))
        #    num_too_long += 1
    LOGGER.info("Sentences: %d" % len(sents))
    LOGGER.info("Sentences too long: %s" % num_too_long)

    # Format sents for CPDQ
    LOGGER.info("Converting to Cheap Bots Done Quick JSON format")
    cbdq_dict = cbdq_json_dict(sents)
    LOGGER.info("Saving JSON to %s" % args.output)
    try:
        with open(args.output, 'w') as file:
            json.dump(cbdq_dict, file, indent=4)
    except IOError as e:
        LOGGER.error("Failed to save to %s: %s" % (args.output, e))
        return e.errno
    return 0

if __name__ == "__main__":
    rtn = main()
    sys.exit(rtn)
