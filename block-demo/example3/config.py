#!/usr/bin/env python
# -*- coding:utf-8 -*-

DESC = "hhhh"
experiment_name = "sr-experiment-29"
TRAIN_ROOT = '/3T/train_tasks/'+experiment_name 

GAN_SETTING = 'DCGAN'    #DCGAN, WGAN
GPU_ID = 1 
GAN_LOSS_FACTOR = 1e-5 #0 1e-5
#CONTENT_LOSS_TYPE="VGG"  #VGG
CONTENT_LOSS_TYPE="NORMAL"  #VGG

epochs = 1000
batch_size = 16 
print_freq_iter = 10 
plot_freq_epoch = 1
snapshot_freq_epoch =  5
snapshot = ''
#snapshot = '/3T/train_tasks/sr-experiment-22/models/snapshot_20.pkl'

#============================================================================================================
def all():
    d = globals()
    ret = {}
    for k in d:
        if not k.startswith("__") and not callable(d[k]):
            ret[k] = d[k]
    return  ret

def printDetail():
    d = all()
    for k in d:
        print(k,' = ',d[k])

if __name__ == "__main__":
    printDetail()
    print (all())
    #Config.printDetail()
