#!/usr/bin/env python
# -*- coding:utf-8 -*-
import torch.utils.data as data
import torch
import torchvision.transforms as transforms
from PIL import Image,ImageFilter
import random
import os
import os.path
import numpy as np
import config


class Dataset(data.Dataset):
    def __init__(self, desc_file_path):
        self.desc_file_path = desc_file_path
        self.image_list = self.read(self.desc_file_path)
        self.toTensor = transforms.ToTensor()

    def __getitem__(self, index):
        file_path= self.image_list[index]
        img = Image.open(file_path)
        w, h = img.width, img.height
        r = max(w*1.0/config.HR_MAX_WIDTH, h*1.0/config.HR_MAX_HEIGHT)
        if r>1:
            hr_img = img.resize((w/r, h/r),  Image.BICUBIC)
        else:
            hr_img = img
        filtered = hr_img.filter(ImageFilter.GaussianBlur(radius=1))
        lr_img = filtered.resize((filtered.width/config.SCALE, filtered.height/config.SCALE),  Image.BICUBIC)
        #lr_img.show()
        #hr_img.show()
        return self.toTensor(lr_img), self.toTensor(hr_img) 

    def __len__(self):
        return len(self.image_list)

    def read(self, filepath):
        import codecs
        result = []
        with codecs.open(filepath, "r", 'utf-8') as myfile:
            for line in myfile:
                line = line.strip()
        #print 'add:', line
                result.append(line.encode('utf-8'))
        print "read from ",filepath, "total:",len(result)
        return result
