#! /usr/bin/env python3

import sys
import os

from collections import defaultdict
import json

from syllables import *

def main():
    counts = defaultdict(list)
    with SyllableCounter() as counter:
        print("Inspecting...")
        for word in counter.logios:
            pron, syll = counter.getPronunciationsAndSyllables(word)
            counts[tuple(syll)].append((word,pron))
    print("Printing...")
    for word,pron in sorted(counts[(1,)]):
        print(word)
    return 0

if __name__ == "__main__":
    rtn = main()
    sys.exit(rtn)
