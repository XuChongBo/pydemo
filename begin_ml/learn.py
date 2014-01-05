#!/usr/bin/python
import random
import os
#from produce_samples import target_fun
import sys

"""
    learn the arguments for y=ax+b
"""

def linear_hypothesis(x,param_dict):
    """
    hypothesis(x)=a*x+b

    input:
        param_dict['a']=123
        param_dict['b']=123
    """
    return param_dict['a']*x+param_dict['b'] 

def loss_fun(index_num,hypothesis,hypoth_param_dict):
    """
    compute the loss for hypothesis(hypoth_param_dict) on the index_num(th) sample set 
    """

    x_file=None
    y_file=None
    loss = 0
    try:
        x_file = file('./data/data%s.x'%index_num)
        y_file = file('./data/data%s.y'%index_num)
        while True:
            x_line = x_file.readline()
            y_line = y_file.readline()
            if not x_line or not y_line:
                break
            sample_x=float(x_line.split()[0])
            sample_y=float(y_line.split()[0])
            loss += (hypothesis(sample_x,hypoth_param_dict)-sample_y)
            #print sample_x, sample_y
    finally:
        if x_file:
            x_file.close()
        if y_file:
            y_file.close()
    return loss    


def loss_derivate(index_num,hypothesis,hypoth_param_dict):
    x_file=None
    y_file=None
    derivate_param1=0 
    derivate_param2=0 
    try:
        x_file = file('./data/data%s.x'%index_num)
        y_file = file('./data/data%s.y'%index_num)
        while True:
            x_line = x_file.readline()
            y_line = y_file.readline()
            if not x_line or not y_line:
                break
            sample_x=float(x_line.split()[0])
            sample_y=float(y_line.split()[0])
            derivate_param1 += (hypothesis(sample_x,hypoth_param_dict)-sample_y)*sample_x
            derivate_param2 += (hypothesis(sample_x,hypoth_param_dict)-sample_y)
            #print sample_x, sample_y
    finally:
        if x_file:
            x_file.close()
        if y_file:
            y_file.close()
    return (derivate_param1,derivate_param2) 

def do_learn():
    """
    get bottom
    """
    param_dict={'a':0,'b':0}
    n=1000
    while n>0:
        n-=1
        #move one step directed by derit 
        loss_derivate()

def save_the_arguments(param_dict):
    try:
        arg_file = open('./arguments.txt', 'w')
        for k in param_dict:
            arg_file.writelines('%s %s ' % (k,param_dict[k]) + os.linesep)
    finally:
        if arg_file:
            arg_file.close()

if __name__ == '__main__':
    #loss_fun(4)
    save_the_arguments({'ab':4, 'xx':34})
    print loss_fun(4,linear_hypothesis,{'a':1,'b':1})
    print loss_fun(4,linear_hypothesis,{'a':1,'b':0})
    print loss_fun(4,linear_hypothesis,{'a':2,'b':0})
    print loss_fun(4,linear_hypothesis,{'a':2,'b':1})
