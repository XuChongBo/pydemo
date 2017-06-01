#!/usr/bin/env python
# -*- coding:utf-8 -*-
import torch
import math
import torchvision
import torch.nn as nn
import torchvision.datasets as dsets
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


class VGG19(nn.Module):
    def __init__(self, num_classes=1000):
        super(VGG19, self).__init__()
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

    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), -1)
        x = self.classifier(x)
        return x

    def __call__(self, *input, **kwargs):
        embedding = torch.zeros(input[0].size(0),512,8,8).cuda()
        def fun(m, i, o): 
            embedding.copy_(o.data)
        #print m
        #print o.data.size()
        hook_handler = self.features[35].register_forward_hook(fun)
        result = super(VGG19, self).__call__(*input, **kwargs)
        #print embedding
        hook_handler.remove()
        return result, Variable(embedding)


