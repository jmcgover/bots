#! /usr/bin/env python3

import os
import sys
import argparse
from argparse import ArgumentParser

import subprocess
import json

from nltk import word_tokenize
from nltk.corpus import cmudict
from string import punctuation
import re

import time

class SyllableCounter():
    JAR_FILENAME = "counter.jar"
    COMMAND = ["java", "-jar", "%s", "%s"]
    ACCEPTED_SYLLABLES = {'AO', 'ER', 'UH', 'EY', 'AY', 
            'AA', 'IH', 'EH', 'IY', 'AW', 'OW', 'OY', 
            'AH', 'UW', 'AE', 'AX'}
    cmu = None
    logios = None
    logiosFilename = "logios.json"
    regexPunctuation = "[" + punctuation + "]"

    # Constructor
    def __init__(self, jarFilename = None, logiosFilename = None, saveLOGIOS = True):
        if jarFilename:
            self.jarFilename = jarFilename
        else:
            self.jarFilename = SyllableCounter.JAR_FILENAME
        SyllableCounter.loadCMUDict()
        if logiosFilename:
            self.logiosFilename = logiosFilename
        else:
            self.logiosFilename = SyllableCounter.logiosFilename
        SyllableCounter.loadLOGIOSDict(self.logiosFilename)
        self.saveLOGIOS = saveLOGIOS
        self.resetTimes()
        return

    # Class Variables
    def isSyllable(phoneme):
        return phoneme[-1].isdigit() or phoneme in SyllableCounter.ACCEPTED_SYLLABLES

    def countSyllablePhonemes(phonemes):
        syllables = 0
        syllables = sum([SyllableCounter.isSyllable(p) for p in phonemes])
        return syllables

    def loadCMUDict():
        if SyllableCounter.cmu is None:
            SyllableCounter.cmu = cmudict.dict()
        return SyllableCounter.cmu

    def loadLOGIOSDict(filename):
        if SyllableCounter.logios is None:
            SyllableCounter.logios = {}
            if os.path.exists(filename):
                with open(filename, "r") as file:
                    SyllableCounter.logios = json.load(file)
        return SyllableCounter.logios

    def saveLOGIOSDict(filename):
        if SyllableCounter.logios is None:
            return False
        with open(filename, "w") as file:
            json.dump(SyllableCounter.logios, file)
        return True

    # With Syntax
    def __enter__(self):
        SyllableCounter.loadCMUDict()
        SyllableCounter.loadLOGIOSDict(self.logiosFilename)
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        self.save()
        return

    # LOGIOS Save
    def save(self):
        SyllableCounter.saveLOGIOSDict(self.logiosFilename)
        return

    # Statistics
    def resetTimes(self):
        self.cmuTime = 0.0
        self.logiosTime = 0.0
        self.cmuLookups = 0
        self.logiosLookups = 0
        return
    def getTimes(self):
        return self.cmuTime, self.logiosTime
    def getAverageTimes(self):
        return self.cmuTime / self.cmuLookups, self.logiosTime / self.logiosLookups
    def getLookups(self):
        print("lookups", self.cmuLookups, self.logiosLookups)
        return self.cmuLookups, self.logiosLookups

    # Known Words
    def isAlreadyKnown(self, word):
        return word in self.cmu or word in self.logios
    def getKnownWords(self):
        return self.cmu.keys()

    # Lookup
    def lookupCMU(self, word):
        # CMU Dictionary
        pronunciations = None
        beginTime = time.time()
        if word in self.cmu:
            pronunciations = self.cmu[word]
            # Timing
            self.cmuTime += time.time() - beginTime
            self.cmuLookups += 1
            return pronunciations
    def lookupLOGIOS(self, word):
        beginTime = time.time()
        # LOGIOS Dictionary
        if word in self.logios:
            pronunciations = self.logios[word]
            self.logiosTime += time.time() - beginTime
            self.logiosLookups += 1
            return pronunciations
        # LOGIOS Lexicon Tool in Java
        command = " ".join(self.COMMAND) % (self.jarFilename, word)
        process = subprocess.Popen(command, shell = True,
                stdout = subprocess.PIPE,
                stderr = subprocess.PIPE
                )
        out, err = process.communicate()
        if err:
            raise Exception("Failed on '%s':%s:%s" % (word,command,err.decode()))
        phones = json.loads(out.decode())
        pronunciations = [phones]
        # Save for future use
        if self.saveLOGIOS:
            self.logios[word] = pronunciations
        # Timing
        self.logiosTime += time.time() - beginTime
        self.logiosLookups += 1
        return pronunciations

    def getPronunciations(self, word):
        if len(word) == 0:
            return []
        # CMU Dictionary
        pronunciations = self.lookupCMU(word)
        if pronunciations:
            return pronunciations
        # LOGIOS Lexicon Lookup
        pronunciations = self.lookupLOGIOS(word)
        return pronunciations
    def formatWord(word):
        # Make Uniform
        word = word.lower().strip()
        # Remove Punctuation
        word = re.sub(SyllableCounter.regexPunctuation, "", word)
        return word
    def getPronunciationsAndSyllables(self, word):
        syllables = []
        # Format
        word = SyllableCounter.formatWord(word)
        # Possible Pronunciations
        pronunciations = self.getPronunciations(word)
        if len(pronunciations) == 0:
            return [], [0]
        # Count Syllables in each Pronunciation
        for pronunciation in pronunciations:
            syllables.append(SyllableCounter.countSyllablePhonemes(pronunciation))
        return pronunciations, syllables
    # Actual Syllables
    def countSyllables(self, word):
        pronunciations, syllables = self.getPronunciationsAndSyllables(word)
        return syllables

from nltk.corpus import brown
def getBrownWords():
    words = []
    words.extend(brown.words())
    return words

from nltk.tokenize import word_tokenize
def getTrumpWords(filename):
    texts = None
    with open(filename) as file:
        texts = json.load(file)
    print("Tokenizing Trump")
    allText = " ".join([m for m in map(lambda x : x["text"], texts)])
    words = word_tokenize(allText)
    return words

def getInsultWords(filename):
    submissions = None
    with open(filename) as file:
        submissions = json.load(file)
    allText = ""
    for s in submissions:
        allText += " ".join((s["title"], s["selftext"]))
    words = word_tokenize(allText)
    return words

def main():
    parser = ArgumentParser(prog=sys.argv[0], description="Counts the number of syllables in a sentence.")
    parser.add_argument("-q", "--quiet",
            default = False,
            action = "store_true",
            help="test it on the brown corpus")
    parser.add_argument("-d", "--different",
            default = False,
            action = "store_true",
            help="counts how many have words have different spellings")
    parser.add_argument("-b", "--brown",
            default = False,
            action = "store_true",
            help="test it on the brown corpus")
    parser.add_argument("-p", "--phonemes",
            default = None,
            nargs = "*",
            help="find the phonemes that have syllables")
    parser.add_argument("words",
            nargs=argparse.REMAINDER,
            default=[],
            help="words to count the syllables of")
    parser.add_argument("-t", "--trump", 
            nargs = 1,
            default = None,
            help = "grabs ngram features for the supplied trump text")
    parser.add_argument("-i", "--insult", 
            nargs = 1,
            default = None,
            help = "grabs ngram features for the supplied insult text")
    args = parser.parse_args()
    words = []
    printPhones = False
    if args.different:
        counter = SyllableCounter()
        for word in sorted(counter.cmu):
            pronunciations, syllables = counter.getPronunciationsAndSyllables(word)
            if len(syllables) > 1:
                if syllables[1:] != syllables[:-1]:
                    print("%s:%s:%s" % (word, syllables, pronunciations))
    if args.brown:
        print("Testing Brown Corpus")
        words.extend(getBrownWords())
    if args.phonemes is not None:
        print("Phonemes and Counting")
        if len(args.phonemes):
            words.extend(args.phonemes)
        printPhones = True
    if len(args.words):
        print("Counting")
        words.extend(args.words)
    if args.trump:
        words.extend(getTrumpWords(args.trump[0]))
    if args.insult:
        words.extend(getInsultWords(args.insult[0]))
    with SyllableCounter(saveLOGIOS = True) as counter:
        totalWords = len(words)
        print("Num Words:%s" % (totalWords,))
        words = set(words)
        uniqueWords = len(words)
        print("Num Unique Words:%s" % (uniqueWords,))
        print("Difference:%s" % (totalWords - uniqueWords,))
        numCounted = 0
        for word in words:
            pronunciations, syllables = counter.getPronunciationsAndSyllables(word)
            if printPhones and not args.quiet:
                print("%s:%s:%s" % (word, pronunciations, syllables))
            elif not args.quiet:
                print("%s:%s" % (word, syllables))
            numCounted += 1
            if numCounted % 10 == 0:
                print("Words So Far:%d" % (numCounted,))
        cmuTime, logiosTime = counter.getTimes()
        cmuLookups, logiosLookups = counter.getLookups()
        totalTime = cmuTime + logiosTime
        totalLookups = cmuLookups + logiosLookups
        print("Type,CMU,LOGIOS, Total")
        print("Time,%.3f,%.3f,%.3f" % (cmuTime, logiosTime, totalTime))
        print("Lookups,%d,%d,%d" % (cmuLookups, logiosLookups, totalLookups))
        cmuAvg = cmuTime / cmuLookups if cmuLookups else 0
        logAvg = logiosTime / logiosLookups if logiosLookups else 0
        totAvg = totalTime / totalLookups if totalLookups else 0
        print("Average Lookup Time,%.3f,%.3f,%.3f" % (cmuAvg, logAvg, totAvg))
    rtn = 0
    return rtn

if __name__ == "__main__":
    rtn = main()
    sys.exit(rtn)
