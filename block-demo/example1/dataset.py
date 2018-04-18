#!/usr/bin/env python
# -*- coding:utf-8 -*-
import torch.utils.data as data
import torch
import torchvision.transforms as transforms
from PIL import Image,ImageFilter
import random
import io
import os
import os.path
import numpy as np
import utils
import config


class Dataset(data.Dataset):
    def __init__(self, desc_file_path):
        self.scale = config.scale 
        self.crop_size = config.hr_size
        self.desc_file_path = desc_file_path
        self.image_list = self.read(self.desc_file_path)
        # Image Preprocessing
        #transforms.Normalize(mean=(0.5, 0.5, 0.5), std=(0.5, 0.5, 0.5))])
        self.randomCrop = utils.MyRandomCrop(self.crop_size, stride=config.crop_stride)
        self.toTensor = transforms.ToTensor()

    def __getitem__(self, index):
        file_path= self.image_list[index]
        image = Image.open(file_path)
        hr_img = self.randomCrop(transforms.Scale(config.precrop_hr_size)(image))
        # sample
        radius =  random.randint(0, 2)
        if radius > 0:
            filtered = hr_img.filter(ImageFilter.GaussianBlur(radius=radius))
        else:
            filtered = hr_img
        # resize
        interpols = (Image.BILINEAR, Image.LANCZOS, Image.NEAREST, Image.BICUBIC)
        inter =  random.randint(0, len(interpols)-1)
        if 1:
            lr_img = filtered.resize((filtered.width/self.scale, filtered.height/self.scale), interpols[inter])
        else:
            filtered  = filtered.filter(ImageFilter.GaussianBlur(radius=1))
            lr_img = filtered.resize((filtered.width/(2*self.scale), filtered.height/(2*self.scale)), interpols[inter])
            lr_img = lr_img.filter(ImageFilter.MedianFilter(size=3))
            lr_img = lr_img.resize((filtered.width/self.scale, filtered.height/self.scale), interpols[inter])

        # jpeg
        qf =  random.randint(75, 95)
        buf = io.BytesIO()
        lr_img.save(buf, format='jpeg', quality=qf)
        lr_img = Image.open(buf)
        # gauss
        if 0:
            lr_img = utils.addGaussRandomNoise(lr_img)
            lr_img = lr_img.filter(ImageFilter.GaussianBlur(radius=random.randint(0, 1)))


        #print "radius:",radius, "iter:", inter
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
