#!/usr/bin/env python

import Image
import numpy as np
import matplotlib.pyplot as plt
import csv

def write_to_csv(pred_list,filename):
    csv_writer = csv.writer(open(filename, "wb"), delimiter=",")
    #csv_writer.writerow(['clo1','colum2','colum3'])
    index=1
    for row in pred_list:
        csv_writer.writerow([index,row])
        index+=1
write_to_csv([23,33,44,55],'./a.csv')

with open("test.csv","w") as csvfile: 
    writer = csv.writer(csvfile)
 
    #先写入columns_name
    writer.writerow(["index","a_name","b_name"])
    #写入多行用writerows
    writer.writerows([[0,1,3],[1,2,3],[2,3,4]])

import csv
with open("test.csv","r") as csvfile:
    reader = csv.reader(csvfile)
    #这里不需要readlines
    for line in reader:
        print line

