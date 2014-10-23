#!/usr/bin/python
# -*- coding: utf-8 -*-
"""This module contains code from
Think Python by Allen B. Downey
http://thinkpython.com

Copyright 2012 Allen B. Downey
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html

"""
import json
import math
import os
import sys
import string
import random
from text_t import  unicode_record_split

entityData={}

def process_file(filename):
    fp = open(filename)
    lines = fp.readlines()
    fp.close()  
    for line in lines:
        words= line.rstrip().split(' ',1)
        entityData[words[0]]=words[1].decode('gbk')
        #raw_input('continue?')
        #continue

    #t = json.loads(a)
    #print words
    #decrip = t.get('description',"")
    #print a.encode('utf8')
    #print d.get('name',None)

def analyze_line(line, order,suffix_map):
    """Reads a line and performs Markov analysis.
    line: string
    order: integer number of words in the prefix
    Returns: map from prefix to list of possible suffixes.
    """
    prefix = ()            # current tuple of words
    word_list= (list)(unicode_record_split(line)) # =line.rstrip()#.split()
    word_list+=[None]  # p(None|x1,x2) the probability x1,x2 end a sentence.
    for word in word_list:
        if len(prefix) < order:
            prefix += (word,)
            continue 

        #suffix_map[prefix].append(word)
        d = suffix_map.setdefault(prefix,{})
        d.setdefault(word,0)
        d[word]+=1;
        prefix = shift(prefix, word)


def match_score(s_map,t_map):
    compound_hist={}
    s_mean=0
    t_mean=0
    for k in s_map.keys():
        tmp=s_map[k]
        for w in tmp.keys():
            s_mean+=tmp[w]
            compound_hist[k+(w,)]=[tmp[w],0]

    for k in t_map.keys():
        tmp=t_map[k]
        for w in tmp.keys():
            t_mean+=tmp[w]
            p = compound_hist.setdefault(k+(w,),[0,0])
            p[1]=tmp[w]

    count = len(compound_hist.keys())
    s_mean=s_mean*1.0/count
    t_mean=t_mean*1.0/count
    #print compound_hist
    xx=0
    yy=0
    xy=0
    for k in compound_hist.keys():
        v=compound_hist[k]
        xx+=(v[0]-s_mean)**2
        yy+=(v[1]-t_mean)**2
        xy+=abs((v[0]-s_mean)*(v[1]-t_mean))
    print 'xx:%s, yy:%s, xy:%s' %(xx,yy,xy)
    divider = math.sqrt(xx)*math.sqrt(yy)
    if abs(divider-0)<0.0000001:
        divider=0.00001
    score = xy/(divider)
    return score

def random_text(n=100):
    """Generates random wordsfrom the analyzed text.

    Starts with a random prefix from the dictionary.

    n: number of words to generate
    """
    # choose a random prefix (not weighted by frequency)
    start = random.choice(suffix_map.keys())
    
    for i in range(n):
        suffixes = suffix_map.get(start, None)
        if suffixes == None:
            # if the start isn't in map, we got to the end of the
            # original text, so we have to start again.
            random_text(n-i)
            return

        # choose a random suffix
        word = random.choice(suffixes)
        print word,
        start = shift(start, word)


def shift(t, word):
    """Forms a new tuple by removing the head and adding word to the tail.

    t: tuple of strings
    word: string

    Returns: tuple of strings
    """
    return t[1:] + (word,)

def printWordMap(w_map):
    #print json.dumps(w_map)
    str=""
    for k1 in w_map.keys():
        str+="{("
        for i in k1:
            str+="%s," % i
            #print w_map[k1]
        str+="): suffix-{"
        for suffix in w_map[k1].keys():
                str+="%s:%s" % (suffix,w_map[k1][suffix])
        str+='}  '        
    print str

if __name__ == '__main__':
    filename='./task1/entity.json'
    benchFileName='./task1/train.txt'
    benchFileName='./task1/test.txt'
    scoreFileName='./score.txt'
    scoreFile = open(scoreFileName,'w')
    n=100
    order=1
    n = int(n)
    order = int(order)
    process_file(filename)
    #random_text(n)
    benchFile = open(benchFileName)
    benchLines = benchFile.readlines()
    benchFile.close()
    for line  in benchLines:
        tmp =line.rstrip().split()
        sID,tID = tmp[0],tmp[1]

        #template='We are now trying to release all our books one month in advance'
        s_map={}
        analyze_line(entityData[sID], order,s_map)
        #print s_map
        print "s_map"
        printWordMap( s_map)

        t_map={}
        analyze_line(entityData[tID], order,t_map)
        print "t_map"
        printWordMap( t_map)

        m = match_score(s_map,t_map)*1.0

        ######0
        score = int(m*4)
        print 'm:%s score:%s' % (m,score)


        ######1
        #nKeys=min(m/len(s_map),len(t_map))
        ##score = int(m*4+0.5)
        #score=int(m*1.4222/nKeys * 4+0.75)
        ##print 'm:%s score:%s' % (m,score)
        #print 'm:%s nKeys:%s score:%s ' % (m,nKeys,score)

        ######2
        #m=(m/len(s_map)+m/len(t_map))/2
        #score = int(m*4+0.5)
        ##score=int(m*1.4222/nKeys * 4+0.75)
        #print 'm:%s score:%s' % (m,score)
        ##print 'm:%s nKeys:%s score:%s ' % (m,nKeys,score)
        

        scoreFile.writelines('%s%s\t%s%s\t%d\n' % (sID,' ',tID,' ',score))
        continue
        str = raw_input('continue?')
        if str=='n':
            break
    scoreFile.close()
