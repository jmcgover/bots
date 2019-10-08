#! /usr/bin/env python3

import sys
import os

import json

def main():
    data = None
    with open("bad_beers.json", 'r') as file:
        data = json.load(file)
    list = []
    list.extend(data["bad_beers"])
    with open("bad_beers.txt", 'w') as outfile:
        for i in list:
            print(i, file=outfile)
    return 0

if __name__ == "__main__":
    rtn = main()
    sys.exit(rtn)
