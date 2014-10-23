#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import copy
import math
import os
import sys
import string
import random
from text_t import  unicode_record_split
from clusterTrain import getBenchDataList
from clusterTrain import cluster

max_order = 2
entityData={}
cluster_list=[]
cluster_map_list=[]
#is_test=True
is_test=False
is_debug=False
is_debug=True

def analyze_line(record_id,tuple_map):
    """
    max_order: 为word_tuple的最大长度
    p(x1)
    p(x2|x1)  note: should inclue  p(None|x1) ??
    p(x3|x1,x2)   note: should include p(None|x1,x2)
    """
    line=entityData[record_id]
    word_list= (list)(unicode_record_split(line)) # =line.rstrip()#.split()
    #word_list+=[None]  # p(None|x1,x2) the probability x1,x2 end a sentence.
    #if is_debug:
    #    printWordList( word_list)
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

def match_score2(s_map,t_map):
    compound_hist={}
    s_sum=0
    t_sum=0
    for k in s_map.keys():
        tmp=s_map[k]
        s_sum+=tmp
        compound_hist[k]=[tmp,0]

    for k in t_map.keys():
        tmp=t_map[k]
        t_sum+=tmp
        p = compound_hist.setdefault(k,[0,0])
        p[1]=tmp

    count = len(compound_hist.keys())
    s_sum*=1.0
    t_sum*=1.0
    s_mean=1.0/count   #TODO  避开0
    t_mean=1.0/count
    if is_debug:
        print "compound_hist"
        printWordHist(compound_hist)
    xx=0
    yy=0
    xy=0
    #s_mean=0
    #t_mean=0
    for k in compound_hist.keys():
        v=compound_hist[k]
        xx+=(v[0]/s_sum-s_mean)**2
        yy+=(v[1]/t_sum-t_mean)**2
        xy+=(v[0]/s_sum-s_mean)*(v[1]/t_sum-t_mean)
    print 'xx:%s, yy:%s, xy:%s' %(xx,yy,xy)
    divider = math.sqrt(xx)*math.sqrt(yy)
    if abs(divider-0)<0.0000001:
        divider=0.0000001
    score = xy/(divider)
    #[-1,1] -> [0,1]
    #return score
    return (score-(-1))/2


def match_score3(s_map,t_map):
    compound_hist={}
    for k in s_map.keys():
        tmp=s_map[k]
        compound_hist[k]=[tmp,0]

    for k in t_map.keys():
        tmp=t_map[k]
        p = compound_hist.setdefault(k,[0,0])
        p[1]=tmp

    count = len(compound_hist.keys())
    if is_debug:
        print "compound_hist"
        printWordHist(compound_hist)
    xy=0
    xx=0
    yy=0
    for k in compound_hist.keys():
        v=compound_hist[k]
        xy+=(v[0])*(v[1])
        xx+=(v[0])*(v[0])
        yy+=(v[1])*(v[1])

    print ' xy:%s' %(xy)
    score = xy/(math.sqrt(xx)*math.sqrt(yy))   # [0,1]
    return score



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
    s_mean=s_mean*1.0/count   #TODO  避开0
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
    #return score
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

def loadEntityData(filename):
    #读取整个实体集
    global entityData
    fp = open(filename)
    lines = fp.readlines()
    fp.close()  
    for line in lines:
        words= line.rstrip().split(' ',1)
        entityData[words[0]]=words[1].decode('gbk')

def get_cluster_map(record_id,r_map):
    for i in range(len(cluster_list)):
        id_set=cluster_list[i]
        if record_id in id_set:
            #isFound=True
            for k in cluster_map_list[i].keys():
                r_map[k]=cluster_map_list[i][k]

            if is_debug:
                print 'found cluster for %s' % record_id
                print r_map
            return
    #if not isFound:
    #如果在train中没有对应的cluster, 则使用record本身的word_map
    if is_debug:
        print 'no cluster for %s' % record_id
    tmp_map={}
    analyze_line(record_id,tmp_map)
    filter_the_map(tmp_map, r_map)
 
def merge_record_mapx(in1_map,in2_map,out_map):
    is_begin=True
    all_keys = in1_map.keys()+in2_map.keys() 
    tmp_map={}
    for k in all_keys:
        if not in1_map:
            v1=1
        else:
            v1 = in1_map.get(k,0)
        v2 = in2_map.get(k,0)
        #tmp_map[k]=v1*v2
        tmp_map[k]=max(v1,v2)
    filter_the_map(tmp_map, out_map)



def merge_record_map(in1_map,in2_map,out_map):
    all_keys = set(in1_map.keys()+in2_map.keys() )
    #tmp_map={}
    str = "k"
    for k in all_keys:
        v1 = in1_map.get(k,0)
        v2 = in2_map.get(k,0)
        #out_map[k]=v1+v2

        if is_debug:
            if str!='k':
                print 'k:', k,v1,v2 
                str = raw_input('continue?')

        if in1_map is {}:
            out_map[k]=v1+v2
        elif v1>0 and v2>0:
            out_map[k]=v1+v2
        #if v1==v2:
        #    tmp_map[k]=(v1+v2)*2
        #tmp_map[k]=max(v1,v2)


def filter_the_map(in_map, out_map):
    for k in in_map.keys():
        #排除频率不大的一元词
        if len(k)==1 and in_map[k]<2:
            continue
        #if len(clu)>2 and tmp_map[k]<2:
        #    continue
        out_map[k]=in_map[k]


def cluster2(train_data_list):
    str=""
    for sID,tID,score in train_data_list:
        if score<4:
            continue
        isFound=False
        for elem in cluster_list:
            if sID in elem or tID in elem:
                elem.add(sID)
                elem.add(tID)
                isFound=True
                break 
        if not isFound:
            cluster_list.append(set([sID,tID]))
     
    if is_debug:
        print 'cluster_list len:', len(cluster_list)
    for clu in cluster_list:
        tmp_map={}
        for id in clu:
            t_map={}
            out_map={} 
            analyze_line(id, t_map)
            merge_record_map(tmp_map,t_map,out_map)
            tmp_map=out_map
        
        clu_map={}
        filter_the_map(tmp_map, clu_map)

        if is_debug:
            print 'tmp_map len:', len(tmp_map) #, t_map
            print 'clu_map len:', len(clu_map)
            str='k'
            if str!='k':
                str = raw_input('continue?')
        cluster_map_list.append(clu_map)


if __name__ == '__main__':
    trainbenchFileName='./task1/train.txt'
    testbenchFileName='./task1/test.txt'
    loadEntityData('./task1/entity.json')

    trainIdSet=set()
    traindata_list = []
    getBenchDataList(trainbenchFileName,traindata_list,trainIdSet)

    testdata_list=[]
    testIdSet=set()
    getBenchDataList(testbenchFileName,testdata_list,testIdSet)

    cluster2(traindata_list)
    print 'cluster num:',len(cluster_list)

    print len(trainIdSet),len(testIdSet)



    scoreFileName='./score.txt'
    scoreFile = open(scoreFileName,'w')
    data_list = traindata_list

    if is_test:
        data_list = testdata_list
    total=len(data_list)
    for idx in range(total):
        elem = data_list[idx]
        sID=elem[0]
        tID=elem[1]
        s=0 
        nIndex=idx+1
        if len(elem)==3:
            s=elem[2]
        print '-------------(%s/%s) --sID-----------' % (nIndex,total)
        s_map={}
        #analyze_line(sID,s_map)
        get_cluster_map(sID,s_map)
        if is_debug:
            print entityData[sID]
            print "s_hist"
            printWordHist( s_map)

        print '-------------(%s/%s) --tID-----------' % (nIndex,total)
        t_map={}
        #analyze_line(tID, t_map)
        get_cluster_map(tID,t_map)
        if is_debug:
            print entityData[tID]
            print "t_hist"
            printWordHist( t_map)


        #进行匹配
        m = match_score3(s_map,t_map)*1.0
        score = int(m*4)

        print '(%s/%s) m:%s score:%s target:%s' % (nIndex,total, m,score,s)
        print '-------------(%s/%s) --end-----------' % (nIndex,total)
        scoreFile.writelines('%s%s\t%s%s\t%d\n' % (sID,' ',tID,' ',score))

        if is_debug:
            str = raw_input('continue?')
            if str=='n':
                break
    scoreFile.close()
