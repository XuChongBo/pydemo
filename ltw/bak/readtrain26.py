#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import math
import os
import sys
import string
import random
from text_t import  unicode_record_split

entityData={}

is_debug=False
#is_debug=True

def analyze_line(line,max_order,tuple_map):
    """
    max_order: 为word_tuple的最大长度
    p(x1)
    p(x2|x1)  note: should inclue  p(None|x1) ??
    p(x3|x1,x2)   note: should include p(None|x1,x2)
    """
    word_list= (list)(unicode_record_split(line)) # =line.rstrip()#.split()
    #word_list+=[None]  # p(None|x1,x2) the probability x1,x2 end a sentence.
    if is_debug:
        printWordList( word_list)
    current_t_list = [()]*max_order

    for word in word_list:  #word 是英文word 或 单个汉字
        for order in range(max_order):
            word_tuple=current_t_list[order]
            if len(word_tuple) < order+1:
                current_t_list[order]+= (word,)
            else:    
                tuple_map.setdefault(word_tuple,0)
                tuple_map[word_tuple]+=1;  #统计word_tuple的出现次数
                current_t_list[order]=shift(word_tuple, word)


def match_score(s_map,t_map):
    compound_hist={}
    s_mean=0
    t_mean=0
    for k in s_map.keys():
        tmp=s_map[k]
        s_mean+=tmp
        compound_hist[k]=[tmp,0]

    for k in t_map.keys():
        tmp=t_map[k]
        t_mean+=tmp
        p = compound_hist.setdefault(k,[0,0])
        p[1]=tmp

    count = len(compound_hist.keys())
    s_mean=s_mean*1.0/count
    t_mean=t_mean*1.0/count
    if is_debug:
        print "compound_hist"
        printWordHist(compound_hist)
    xx=0
    yy=0
    xy=0
    s_mean=0
    t_mean=0
    for k in compound_hist.keys():
        v=compound_hist[k]
        xx+=(v[0]-s_mean)**2
        yy+=(v[1]-t_mean)**2
        xy+=(v[0]-s_mean)*(v[1]-t_mean)
    print 'xx:%s, yy:%s, xy:%s' %(xx,yy,xy)
    divider = math.sqrt(xx)*math.sqrt(yy)
    if abs(divider-0)<0.0000001:
        divider=0.00001
    score = xy/(divider)
    #[-1,1] -> [0,1]
    return (score-(-1))/2


def shift(t, word):
    """Forms a new tuple by removing the head and adding word to the tail.

    t: tuple of strings
    word: string

    Returns: tuple of strings
    """
    return t[1:] + (word,)

def printWordList(word_list):
    print "=====wordlist begin==="
    str="["
    for w in word_list:
        str+="%s," % w
    str+="]"
    print str
    print "=====wordlist end==="


def printWordHist(w_map):
    print "=====hist begin==="
    str="{"
    for k1 in w_map.keys():
        str+="%s:%s, " % ("".join(k1),w_map[k1])
    str+='}'        
    print str
    print "=====hist end==="

if __name__ == '__main__':
    filename='./task1/entity.json'
    benchFileName='./task1/train.txt'
    #benchFileName='./task1/test.txt'
    scoreFileName='./score.txt'
    scoreFile = open(scoreFileName,'w')
    n=100
    max_order = 2

    #读取整个实体集
    fp = open(filename)
    lines = fp.readlines()
    fp.close()  
    for line in lines:
        words= line.rstrip().split(' ',1)
        entityData[words[0]]=words[1].decode('gbk')


    benchFile = open(benchFileName)
    benchLines = benchFile.readlines()
    benchFile.close()
    nIndex=1
    total=len(benchLines)
    for line  in benchLines:
        tmp =line.rstrip().split()
        sID,tID = tmp[0],tmp[1]
        s_map={}
        analyze_line(entityData[sID], max_order,s_map)
        if is_debug:
            print entityData[sID]
            print "s_hist"
            printWordHist( s_map)

        t_map={}
        analyze_line(entityData[tID], max_order,t_map)
        if is_debug:
            print entityData[tID]
            print "t_hist"
            printWordHist( t_map)

        #获取context, 筛选words
        #filter_record_map(sID,s_map)
        #filter_record_map(tID,t_map)

        #进行匹配
        m = match_score(s_map,t_map)*1.0

        ######0
        score = int(m*4)
        print '(%s/%s) m:%s score:%s' % (nIndex,total, m,score)
        nIndex+=1

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
