#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os

s1= "hello word"
s2 = "the world is beatiful."
s3 = "you are beatiful."

#字典表
wordTable=['', 'a', 'b', 'bc', ' b']

#
#every note 作为一种概念.  第二元素作为第一个元素的预测
tupleNodeHeap =[(0,1),(1,2),]

ltw = [(3,5),(0,19),(1,1),(2,7),(7,0)]
print a
#运作时,predict 和 transmit交叉进行.  

#predict完后设置node的为预测状态.   transmit发生时发生match后，比较上下的值，再决定是否往上transmit

#比较的值，来自历史的强度积累


# sort from min to max.   It's non-inplace operation
b = sorted(a, key=lambda x:x[0])
print b


def myfun(x):
    return x[0]**2+x[1]**2
c = sorted(a, key=myfun)
print c 

# sort from max to min
d = sorted(a, key=myfun,reverse=True)
print d
