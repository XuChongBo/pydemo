#!/usr/bin/env python
# -*- coding:utf-8 -*-
import torch
import math
import torchvision
import torch.nn as nn
import torchvision.datasets as dsets
import torchvision.transforms as transforms
import config
import dataset 
from torch.autograd import Variable
#https://discuss.pytorch.org/t/how-to-perform-finetuning-in-pytorch/419/19

def make_layers(batch_norm=False):
    cfg = [64, 64, 'M', 128, 128, 'M', 256, 256, 256, 256, 'M', 512, 512, 512, 512, 'M', 512, 512, 512, 512, 'M']
    layers = []
    in_channels = 3
    for v in cfg:
        if v == 'M':
            layers += [nn.MaxPool2d(kernel_size=2, stride=2)]
        else:
            conv2d = nn.Conv2d(in_channels, v, kernel_size=3, padding=1)
            if batch_norm:
                layers += [conv2d, nn.BatchNorm2d(v), nn.ReLU(inplace=True)]
            else:
                layers += [conv2d, nn.ReLU(inplace=True)]
            in_channels = v
    return nn.Sequential(*layers)


class VGG19Feature(nn.Module):
    def __init__(self, num_classes=1000):
        super(VGG19Feature, self).__init__()
        self.features = make_layers()
        self.classifier = nn.Sequential(
            nn.Linear(512 * 7 * 7, 4096),
            nn.ReLU(True),
            nn.Dropout(),
            nn.Linear(4096, 4096),
            nn.ReLU(True),
            nn.Dropout(),
            nn.Linear(4096, num_classes),
        )
        self.load_state_dict(torch.load('vgg19-dcbb9e9d.pth'))
        self.features = nn.Sequential( *list(self.features.children())[:-1])
        print self.features
#        print self.features

    def normalize(self, x):
        # TODO: make efficient
        mean=[0.485, 0.456, 0.406]
        std=[0.229, 0.224, 0.225]
        y = Variable(torch.zeros(x.size()).cuda())
        i = 0
        for xi, m, s in zip(x, mean, std):
            y[i] = xi.sub(m).div(s)
            i+=1
        #print 'y max:', y.max()
        return y

    def forward(self, x):
        x = self.normalize(x)
        x = self.features(x)
        x = x.view(x.size(0), -1)
        return x

# test output size
if __name__ == "__main__":
    images = Variable(torch.ones(2, 3, config.hr_size, config.hr_size))
    vgg = VGG19Feature()
    vgg.cuda()
    print "do forward..."
    outputs = vgg(images)
    print (outputs.size())   # (10, 100)
    print torch.max(outputs)
