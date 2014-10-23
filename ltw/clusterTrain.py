#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import math
import os
import sys
import string
import random
from text_t import  unicode_record_split

#is_debug=False
is_debug=True





#entityData={}

def getBenchDataList(filename,datalist,idSet):
    benchFile = open(filename)
    benchLines = benchFile.readlines()
    benchFile.close()
    nIndex=1
    total=len(benchLines)
    for line  in benchLines:
        tmp =line.rstrip().split()
        if len(tmp)==3:
            sID,tID,score = tmp[0],tmp[1],int(tmp[2])
            datalist.append((sID,tID,score))
            idSet.add(sID)
            idSet.add(tID)
        else:
            sID,tID= tmp[0],tmp[1]
            datalist.append((sID,tID))
            idSet.add(sID)
            idSet.add(tID)


def cluster(data_list,stat_list):
    for record in data_list:
        sID,tID,score=record
        if score<4:
            continue
        isFound=False
        for elem in stat_list:
            if sID in elem['ids'] or tID in elem['ids']:
                elem['ids'].add(sID)
                elem['ids'].add(tID)
                elem[(sID,tID)]=score
                isFound=True
                break 
        if not isFound:
            stat_list.append({(sID,tID):score,'ids':set([sID,tID])})
        #print stat_list
        #print '(%s/%s) sID:%s,tID:%s,scor:%s ' % (nIndex,total, sID,tID,score)
        continue
        str = raw_input('continue?')
        if str=='n':
            break
    nIndex=1
    maxCount=0
    for k in stat_list:
        l = len(k['ids'])
        #print nIndex, l
        if  l>maxCount:
            maxCount=l
            print nIndex, l
        nIndex+=1
    print "total num: ", len(stat_list)

if __name__ == '__main__':
    benchFileName='./task1/train.txt'
    testbenchFileName='./task1/test.txt'

    trainIdSet=set()
    data_list = []
    getBenchDataList(benchFileName,data_list,trainIdSet)

    testdata_list=[]
    testIdSet=set()
    getBenchDataList(testbenchFileName,testdata_list,testIdSet)

    stat_list=[]
    cluster(data_list,stat_list)

    print len(trainIdSet),len(testIdSet)

    #for id in testIdSet:
    #    if id in trainIdSet:
    #        print 'ok'
    
    #找context
    for id in testIdSet:
        nIndex=0
        for clu in stat_list:
            if id in clu['ids'] :
                print nIndex,'ok',len(clu['ids'])
            nIndex+=1

    for sID,tID in testdata_list:
        print sID, tID 
        #if sID in stat_list
        str = raw_input('continue?')
        if str=='n':
            break
