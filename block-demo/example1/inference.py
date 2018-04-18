#!/usr/bin/env python
# -*- coding:utf-8 -*-
import argparse
import os
import shutil
import traceback
import time
import glob
from PIL import Image,ImageFilter
from scipy.misc import imresize
import sys
from G import  Generator
import utils
from torch.autograd import Variable
import torch
import torch.nn as nn
import torch.nn.parallel
import torch.backends.cudnn as cudnn
import torch.optim
import torch.utils.data
import torchvision.transforms as transforms
import torchvision

def touchDir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

g = None
trans = None
scale = 2
gpu_id = 0

if gpu_id is not None:
    print "use gpu"
    cudnn.benchmark = True
    torch.cuda.set_device(gpu_id)

def doSR(img, args):
    global g, trans
    if not g or not trans:
        g = Generator()
        print "load model"
        checkpoint = torch.load(args.snapshot, map_location=lambda storage, loc: storage)
        print checkpoint['G_model'].keys()
        g.load_state_dict(checkpoint['G_model'])
        start_time = time.time()
        if gpu_id is not None:
            print "send gpu"
            g.cuda()
        g.eval()
        trans = transforms.Compose([transforms.ToTensor(), ])
    # inference
    print "model already."
    lr_img = trans(img)

    lr_imgs = lr_img.view(1, lr_img.size(0), lr_img.size(1), lr_img.size(2))
    lr_imgs = Variable(lr_imgs, volatile=True)
    if gpu_id is not None:
        lr_imgs = lr_imgs.cuda()
    end_time = time.time()
    print " load cost:%s ms" % int((end_time-start_time)*1000)

    print "inference.."
    start_time = time.time()
    sr_imgs = g(lr_imgs)
    end_time = time.time()
    print " cost:%s ms" % int((end_time-start_time)*1000)

    if gpu_id is not None:
        sr_imgs = sr_imgs.cpu()
    return sr_imgs

def inferenceDir(args, root_dir, save_dir, exts=['.jpg','.png']):
    root_dir = root_dir.rstrip("/")
    i = 0
    for root, dirs, files in os.walk(root_dir):
        for filename in files:
            #if filename.endswith('.'+ext):
            if filename[-4:] in exts:
                i += 1
                image_path = os.path.join(root, filename)
                print i, image_path
                try:
                    inferenceOne(args, image_path, save_dir)
                except Exception,e:
                    print "Exception happens:", e
                    print traceback.format_exc()
                    time.sleep(2)

def inferenceOne(args, img_path, save_dir):
    #read image
    img = Image.open(img_path)
    width, height =  img.size
    print width, height
    sr_imgs = doSR(img, args)

    if 0:
        """
        sr_img  = transforms.ToPILImage()(sr_imgs.data[0])
        sr_img= sr_img.resize((width, height),  Image.NEAREST)
        sr_img = transforms.ToTensor()(sr_img)
        """
        sr_img = sr_imgs.data[0][:, 0::2, 0::2]
        img = transforms.ToTensor()(img)[0:sr_img.size(0), 0:sr_img.size(1)]
        print "sr size", sr_img.size()
        print "img size", img.size()
        torchvision.utils.save_image(torch.stack((img,sr_img),0), os.path.join(save_dir, os.path.basename(img_path)) )
    else:
        img = img.resize((width*2, height*2),  Image.BICUBIC)
        img = transforms.ToTensor()(img)
        torchvision.utils.save_image(torch.stack((img,sr_imgs.data[0]),0), os.path.join(save_dir, os.path.basename(img_path)) )
    #torchvision.utils.save_image()
    """
    if need_preprocess:
        hr_dir = save_dir[:-2]+"hr"
        touchDir(hr_dir)
        hr_img.save(os.path.join(hr_dir, os.path.basename(img_path)))
    """


def inferenceDesc(args, filepath, save_dir):
    import codecs
    with codecs.open(filepath, "r", 'utf-8') as myfile:
        i = 0
        for line in myfile:
            i += 1
            #line = line.strip()
            image_path = line.strip().encode('utf-8')
            print i, image_path
            try:
                inferenceOne(args, image_path, save_dir)
            except Exception,e:
                print "Exception happens:", e
                print traceback.format_exc()
                time.sleep(2)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='PyTorch SRGAN Inference')
    parser.add_argument('--imagepath', default='./36.png', type=str, metavar='PATH',
                        help='path to images for test')
    parser.add_argument('--save-dir', default='/tmp/', type=str, metavar='PATH',
                        help='path to save results')
    parser.add_argument('--snapshot', default='/3T/train_tasks/sr-experiment-27/models/snapshot_590.pkl', type=str, metavar='PATH',
                        help='path to latest checkpoint ')
    #parser.add_argument('--need-preprocess', action="store_true", default=need_preprocess,  help='')
    args = parser.parse_args()
    print  args
    raw_input("press anykey ") 
    touchDir(args.save_dir)
    if  os.path.isfile(args.imagepath):
        if args.imagepath[-4:]=='.txt':
            inferenceDesc(args, args.imagepath, args.save_dir)
        else:
            inferenceOne(args, args.imagepath, args.save_dir)
    else:
        inferenceDir(args, args.imagepath, args.save_dir)
