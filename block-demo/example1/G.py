#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Implementation of https://arxiv.org/pdf/1512.03385.pdf.
# See section 4.2 for model architecture on CIFAR-10.
# Some part of the code was referenced below.
# https://github.com/pytorch/vision/blob/master/torchvision/models/resnet.py
import torch 
import torch.nn as nn
import math
from torch.autograd import Variable
import utils

# Residual Block
class ResidualBlock(nn.Module):
    def __init__(self):
        super(ResidualBlock, self).__init__()
        self.conv1 = nn.Conv2d(64, 64, kernel_size=3, stride=1, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(64)
        self.relu = nn.ReLU(inplace=True)
        self.conv2 = nn.Conv2d(64, 64, kernel_size=3, stride=1, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(64)
        
    def forward(self, x):
        residual = x
        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)
        out = self.conv2(out)
        out = self.bn2(out)
        out += residual
        #out = self.relu(out)
        return out

class Generator(nn.Module):

    def __init__(self):
        super(Generator, self).__init__()
        self.conv1 = nn.Conv2d(3, 64, kernel_size=3, stride=1, padding=1, bias=False)
        self.relu1 = nn.ReLU(True)

        self.blocks =  self.make_blocks_(16)
        self.conv2 = nn.Conv2d(64, 64, kernel_size=3, stride=1, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(64)

        self.upsample= nn.Sequential(
            nn.Conv2d(64, 256, kernel_size=3, stride=1, padding=1, bias=False),
            nn.UpsamplingNearest2d(scale_factor=2),
            nn.Conv2d(256, 256, kernel_size=3, stride=1, padding=1, bias=False),
            nn.ReLU(True),
            nn.Conv2d(256, 3, kernel_size=3, stride=1, padding=1, bias=False)
        )
        self.weights_init()

#class torch.nn.Conv2d(in_channels, out_channels, kernel_size, stride=1, padding=0, dilation=1, groups=1, bias=True)
#Hout=floor((Hin+2∗padding[0]−dilation[0]∗(kernel_size[0]−1)−1)/stride[0]+1)


    def make_blocks_(self, num):
        layers = []
        for i in range(num):
            layers.append(ResidualBlock())
        return nn.Sequential(*layers)
    

    def forward(self, x):
        # stage 1
        conv1 = self.conv1(x)
        relu1 = self.relu1(conv1)

        # stage 2
        residual = relu1
        blocks_out = self.blocks(relu1)
        conv2 = self.conv2(blocks_out)
        bn2 = self.bn2(conv2)
        out2 = bn2+residual 

        # stage 3 
        out3 = self.upsample(out2)

        return out3



    def weights_init(self):
        for idx, m in enumerate(self.modules()):
            classname = m.__class__.__name__
            #print(idx, '->', classname)
            if classname.find('Conv') != -1:
                m.weight.data.normal_(0.0, 0.02)
            elif classname.find('BatchNorm') != -1:
                m.weight.data.normal_(1.0, 0.02)
                m.bias.data.fill_(0)
            elif classname.find('Linear') != -1:
                m.weight.data.normal_(0, 0.01)
                m.bias.data.zero_()
# test output size
if __name__ == "__main__":
    images = Variable(torch.randn(1, 3, 256, 256), volatile=True)
    print type(images.data)
    g = Generator()
    utils.memory_used(g, images)    
    images2 = Variable(torch.randn(1, 3, 256, 256))
    utils.memory_used(g, images2)    
    import config
    g.cuda(config.GPU_ID)
    print ("do forward...")
    outputs = g(images.cuda(config.GPU_ID))
    print ("after")


    if 0:
        print ("do forward...")
        outputs = g(images)
        print (outputs.size())   # (10, 100)




