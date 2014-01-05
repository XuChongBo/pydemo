#!/usr/bin/env python

import Image
import numpy as np
import matplotlib.pyplot as plt
import csv

def read_test_data_to_ndarray(filname="../data/test.csv", limit=None):
    print "Reading train data"
    data = []
    csv_reader = csv.reader(open(filname, "r"), delimiter=",")
    index = 0
    for row in csv_reader:
        index += 1
        if index == 1:
            continue
        data.append(np.float32(row)/255)
        if limit != None and index == limit + 1:
            break
    data_x=np.asarray(data)        
    #print data_x,data_x.shape,data_x.dtype,type(data_x)
    return data_x
read_test_data_to_ndarray(limit=4)
exit(0)


def read_data_to_ndarray(filname="../data/train.csv", limit=None):
    print "Reading train data"
    data = []
    labels = []
    csv_reader = csv.reader(open(filname, "r"), delimiter=",")
    index = 0
    for row in csv_reader:
        index += 1
        if index == 1:
            continue
        labels.append(int(row[0]))
        row = row[1:]
        data.append(np.float32(row)/255)
        if limit != None and index == limit + 1:
            break
    data_x=np.asarray(data)        
    data_y=np.asarray(labels,dtype=np.int32)
    """
    print data_x,data_x.dtype,type(data_x),data_y,type(data_y),data_y.dtype
    print data_x[1,126],data[1][126],data_y[3],labels
    #print data,labels, data[0].shape
    #print data_x,type(data_x),data_x[1]
    #print data_x,type(data_x),data_y,type(data_y)
    #print data_x[1,126],data[1][126],data_y[3],labels
    """
    return (data_x, data_y)
read_data_to_ndarray(limit=4)


exit(0)
def read_data(filname, limit=None):
    data = []
    labels = []
    csv_reader = csv.reader(open(filname, "r"), delimiter=",")
    index = 0
    for row in csv_reader:
        index += 1
        if index == 1:
            continue

        labels.append(int(row[0]))
        row = row[1:]
        data.append(np.array(np.int64(row)))
        if limit != None and index == limit + 1:
            break
    return (data, labels)

print "Reading train data"
train, target = read_data("../data/train.csv",1)



print train[0].shape, train[0].dtype
data=train[0].astype(np.uint8)
print data.shape, data.dtype
data=np.reshape(data, (28, 28))
print data.shape, data.dtype
img = Image.fromarray(data)
#img = PIL.Image.fromarray(data)
img.show()

#img.save('my.png')
