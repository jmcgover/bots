#! /usr/bin/env python3

import sys
import os

import json

from argparse import ArgumentParser

DESCRIPTION = """Get all beer types from Untappd"""
def get_arg_parser():
    parser = ArgumentParser(prog=sys.argv[0], description=DESCRIPTION)
    parser.add_argument(
            metavar = "<styles.txt>",
            default = None,
            dest = "styles_filename",
            help = "path to line delimited file of styles")
    parser.add_argument(
            metavar = "<flavor.txt>",
            default = None,
            dest = "flavors_filename",
            help = "path to line delimited file of flavors")
    parser.add_argument(
            metavar = "<weights.txt>",
            default = None,
            dest = "weights_filename",
            help = "path to line delimited file of weights")
    parser.add_argument(
            metavar = "<aged.txt>",
            default = None,
            dest = "aged_filename",
            help = "path to line delimited file of aged designators")
    return parser

def file_to_arr(file):
    array = []
    for line in file:
        array.append(line.strip())
    return array

def main():
    parser = get_arg_parser()
    args = parser.parse_args()

    styles = []
    with open(args.styles_filename, 'r') as file:
        styles = file_to_arr(file)
    flavors = []
    with open(args.flavors_filename, 'r') as file:
        flavors = file_to_arr(file)
    weights = []
    with open(args.weights_filename, 'r') as file:
        weights = file_to_arr(file)
    aged = []
    with open(args.aged_filename, 'r') as file:
        aged = file_to_arr(file)

    cbdq = {}
    cbdq["origin"] = ["#weights# #aged# #flavors# #styles#"]
    cbdq["styles"] = styles
    cbdq["flavors"] = flavors
    cbdq["weights"] = weights
    cbdq["aged"] = aged

    with open("cbdq.json", 'w') as outfile:
        json.dump(cbdq, outfile, sort_keys=True, indent=4)
    return 0

if __name__ == "__main__":
    rtn = main()
    sys.exit(rtn)
