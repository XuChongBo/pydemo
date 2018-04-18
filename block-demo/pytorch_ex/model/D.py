#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import print_function
import torch
import math
import torchvision
import torch.nn as nn
import torchvision.datasets as dsets
from torch.autograd import Variable
import config
config.printDetail()
raw_input("xx")
"""
def forward_hook(module, input, output):
    print('---------- forward ----------')
    print(module)
    print "forward_in:", input[0].data[0]
    print "forward_out:", output[0].data[0]  

#for val in input:
#    print("input val:",val)
#for out_val in output:
#    print("output val:", out_val)    

def backward_hook(module, grad_in, grad_out):
    print '---------- backward ----------'
    print(module)
    print 'grad_in:', grad_in[0].data[0]
    print 'grad_out', grad_out[0].data[0]
    for param in module.parameters():
        print 'param:', param
        print 'param grad:', param.grad
"""
# Discriminator Model
class Discriminator(nn.Module):
    def __init__(self):
        super(Discriminator, self).__init__()
        self.features = nn.Sequential(
            # input is (nc) x 64 x 64
            nn.Conv2d(3, 64, kernel_size=3, stride=1, padding=1, bias=False),
            nn.LeakyReLU(0.2, inplace=True),

            # state size. (ndf) x 32 x 32
            nn.Conv2d(64, 64, kernel_size=3, stride=2, padding=1, bias=False),
            nn.LeakyReLU(0.2, inplace=True),
            nn.BatchNorm2d(64),
            # state size. (ndf*2) x 16 x 16
            nn.Conv2d(64, 128, kernel_size=3, stride=1, padding=1, bias=False),
            nn.LeakyReLU(0.2, inplace=True),
            nn.BatchNorm2d(128),

            nn.Conv2d(128, 128, kernel_size=3, stride=2, padding=1, bias=False),
            nn.LeakyReLU(0.2, inplace=True),
            nn.BatchNorm2d(128),

            nn.Conv2d(128, 256, kernel_size=3, stride=1, padding=1, bias=False),
            nn.LeakyReLU(0.2, inplace=True),
            nn.BatchNorm2d(256),

            nn.Conv2d(256, 256, kernel_size=3, stride=2, padding=1, bias=False),
            nn.LeakyReLU(0.2, inplace=True),
            nn.BatchNorm2d(256),

            nn.Conv2d(256, 512, kernel_size=3, stride=1, padding=1, bias=False),
            nn.LeakyReLU(0.2, inplace=True),
            nn.BatchNorm2d(512),

            nn.Conv2d(512, 512, kernel_size=3, stride=2, padding=1, bias=False),
            nn.LeakyReLU(0.2, inplace=True),
            nn.BatchNorm2d(512)
        )
        if config.hr_size == 128:
            n = 32768
        elif config.hr_size == 768:
            n = 73728 
        elif config.hr_size == 512:
            n = 524288 
        else:
            raise RuntimeError('hr_size %s is not surpported by D' % config.hr_size)
        self.classifier = nn.Sequential(
            nn.Linear(n, 1024),  
            nn.LeakyReLU(inplace=True),
            nn.Linear(1024, 1)
        )
        if config.GAN_SETTING in ["WGAN","LSGAN"]:
            pass
        else:
            self.classifier.add_module('sigmoid',nn.Sigmoid())
        self.weights_init()
        """
        self.classifier[2].register_forward_hook(forward_hook)
        self.classifier[2].register_backward_hook(backward_hook)
        self.classifier[3].register_forward_hook(forward_hook)
        self.classifier[3].register_backward_hook(backward_hook)
        """
        # Freeze these weights # If you want to finetune only top layer of the model.
        #for p in self.features.parameters():
        #   p.requires_grad = False

    def forward(self, x):
        out = self.features(x)
        out = out.view(out.size(0), -1)
        out = self.classifier(out)
        return out

    def weights_init(self):
        for idx, m in enumerate(self.modules()):
            classname = m.__class__.__name__
            print(idx, '->', classname)
            if classname.find('Conv') != -1:
                m.weight.data.normal_(0.0, 0.02)
            elif classname.find('BatchNorm') != -1:
                m.weight.data.normal_(1.0, 0.02)
                m.bias.data.fill_(0)

    
# 4x4 Transpose convolution
#Hout = (Hin−1)∗stride[0]−2∗padding[0]+kernel_size[0]+output_padding[0]

# test output size
if __name__ == "__main__":
    images = Variable(torch.randn(1, 3, config.hr_size, config.hr_size))
    d = Discriminator()
    print("do forward...")
    outputs = d(images)
    print (outputs.size())   # (10, 100)
