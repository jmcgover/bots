#! /usr/bin/env python3

import sys
import os

import json

from argparse import ArgumentParser

DESCRIPTION = """Get all beer types from Untappd"""
def get_arg_parser():
    parser = ArgumentParser(prog=sys.argv[0], description=DESCRIPTION)
    parser.add_argument(
            metavar = "<auth.json>",
            default = None,
            dest = "auth_filename",
            help = "path to JSON file of Untappd API authorization")
    return parser

def main():
    parser = get_arg_parser()
    args = parser.parse_args()
    client_id = None
    client_secret = None
    with open(args.auth_filename, 'r') as file:
        auth = json.load(file)
        client_id = auth["client_id"]
        client_secret = auth["client_secret"]
    print("client_id:", client_id)
    print("client_secret:", client_secret)
    return 0

if __name__ == "__main__":
    rtn = main()
    sys.exit(rtn)
