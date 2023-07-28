#convert dictionary to openutau format
#The input file should be in UTF-8 encoding

import sys
import os
from typing import List, Dict, Tuple
import yaml

extra_separators:List[str] = ["|"]

def guess_phoneme_type(entries: Dict[str, List[str]]) -> Tuple[List[str], List[str]]:
    #Get all the phonemes and guess if each phoneme is a vowel or consonant
    #This applies to two-part dictionaries only, like Chinese and Japanese
    #output: (vowel list, consonant list)
    heads:Dict[str,int] = {}#how many times a phoneme is at the beginning of a word
    tails:Dict[str,int] = {}#how many times a phoneme is at the end of a word
    for key, value in entries.items():
        for ph in value:
            heads[ph] = heads.get(ph, 0)
            tails[ph] = tails.get(ph, 0)
        heads[value[0]] += 1
        tails[value[-1]] += 1
    vowels:List[str] = ["SP", "AP"]
    consonants:List[str] = []
    #if a phoneme is at the end of a word more often, then it is probably a vowel
    for key in heads.keys():
        if heads[key] <= tails[key]:
            vowels.append(key)
        else:
            consonants.append(key)
    return (vowels, consonants)

def convert(inputFile: str, outputFile: str):
    entries:Dict[str, List[str]] = {"SP":["SP"], "AP":["AP"]}#special phonemes
    with open(inputFile, 'r', encoding="UTF8") as f:
        lines = f.readlines()
    #convert entries
    for line in lines:
        for c in extra_separators:
            line = line.replace(c, ' ')
        line = line.strip()
        if line == '':
            continue
        line = line.split()
        if len(line) < 2:
            continue
        key = line[0]
        value = line[1:]
        entries[key] = value
    (vowels, consonants) = guess_phoneme_type(entries)
    print("Phoneme type guessed from the dictionary:")
    print("vowels:", vowels)
    print("consonants:", consonants)
    print("Please check if the guess is correct. If not, please edit the dictionary manually.")
    output={
        "symbols":
            [{"symbol":ph,"type":"vowel"} for ph in vowels]
            + [{"symbol":ph,"type":"fricative"} for ph in consonants],
        "entries":[{"grapheme":key, "phonemes":value} for key, value in entries.items()]
    }

    with open(outputFile, 'w', encoding="UTF8") as f:
        yaml.dump(output, f, allow_unicode=True)

def main():
    if(len(sys.argv)<1):
        print("Input file:")
        inputFile = input()
    else:
        inputFile = sys.argv[1]
        print("Input file:", inputFile)
    if(len(sys.argv)<2):
        print("Output file:")
        outputFile = input()
    else:
        outputFile = sys.argv[2]
        print("Output file:", outputFile)
    convert(inputFile, outputFile)

if(__name__=="__main__"):
    main()