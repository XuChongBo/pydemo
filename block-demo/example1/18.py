#!/usr/bin/env python
# -*- coding:utf-8 -*-

experiment_name = "sr-experiment-18"
DESC = "只用gauss, sigma=randint(0,2), 不用jpeg"
GAN_SETTING = 'DCGAN'    #DCGAN, WGAN
GPU_ID = 1
TRAIN_ROOT = '/3T/train_tasks/'+experiment_name 
GAN_LOSS_FACTOR = 1e-5  #0
CONTENT_LOSS_TYPE="NORMAL"  #VGG
epochs = 1000
batch_size = 20
print_freq_iter = 10 
plot_freq_epoch = 1
snapshot_freq_epoch =  5
snapshot = ''
evaluate = False


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
        print k,' = ',d[k]

if __name__ == "__main__":
    printDetail()
    print all()
#Config.printDetail()
