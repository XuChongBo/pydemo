"""This module contains code from
Think Python by Allen B. Downey
http://thinkpython.com

Copyright 2012 Allen B. Downey
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html

"""
import json
import math
import sys
import string
import random

# global variables
suffix_map = {}        # map from prefixes to a list of suffixes


def distance(benchFileName, scoreFileName):
    benchFile = open(benchFileName)
    scoreFile = open(scoreFileName)
    benchLines = benchFile.readlines()
    scoreLines = scoreFile.readlines()
    count = len(benchLines)
    s=0
    for i in range(count):
        a= benchLines[i].rstrip().split()
        b= scoreLines[i].rstrip().split()
        s+= (int(a[2])-int(b[2]))**2
    return math.sqrt(s)

if __name__ == '__main__':
    benchFileName='./task1/train.txt'
    #benchFileName='./c.txt'
    scoreFileName='./score.txt'
    
    d = distance(benchFileName, scoreFileName)
    print d

    #random_text(n)

