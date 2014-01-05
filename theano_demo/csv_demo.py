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

