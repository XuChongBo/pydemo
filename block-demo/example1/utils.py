#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os.path
import sys
import socket
import random
import numbers
from PIL import ImageOps
import requests
from urlparse import urlparse
import cStringIO
import PIL.Image
from PIL import Image
from visdom import Visdom
import numpy as np
import config
import pynvml 
pynvml.nvmlInit()

vis = Visdom()

all_wins = {}


def plot(title, name, i, v):
    win = all_wins.get(title, None) 
    if win is None:
        win = vis.line(env=config.experiment_name, X=np.array([i]), Y=np.array([v]), opts={'legend':[name], 'title':title})
        all_wins[title] = win
    else:
        vis.updateTrace(env=config.experiment_name, win=win,  X=np.array([i]), Y=np.array([v]), name=name)
    #viz.image( np.random.rand(3,64, 64), win="abxxx", opts=dict(title='sr', caption='sr images'))


def plotText():
    txt = ""
    d = config.all()
    for k in d:
        txt += "%s = %s </br>" % (k, d[k])
    vis.text(txt, win='ttt', env=config.experiment_name)


def printModel(model):

    for idx, m in enumerate(model.modules()):
        print(idx, '->', m)

def touchDir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def createLink(src, dst):
    if not os.path.lexists(dst):
        os.symlink(src, dst)

def getNetworkIp():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.connect(('<broadcast>', 0))
    return s.getsockname()[0]


def prepareDirs():
    # assure 
    config.MODEL_FOLDER=os.path.join(config.TRAIN_ROOT, 'models')
    config.LR_FOLDER=os.path.join(config.TRAIN_ROOT, 'lr')
    config.HR_FOLDER=os.path.join(config.TRAIN_ROOT, 'hr')
    config.SR_FOLDER=os.path.join(config.TRAIN_ROOT, 'sr')
    config.PEEK_FOLDER=os.path.join(config.TRAIN_ROOT, 'peek')
    config.TEST_FOLDER=os.path.join(config.TRAIN_ROOT, 'test')
    touchDir(config.MODEL_FOLDER)
    dirs = (("Train LR", config.LR_FOLDER), ("Train HR",config.HR_FOLDER), ("Train SR",config.SR_FOLDER), ("Peek",config.PEEK_FOLDER), ("Test",config.TEST_FOLDER))
    txt = ""
    IP = getNetworkIp()
    for title, dirpath in dirs:
        touchDir(dirpath)
        dirname = dirpath.rstrip("/").split('/')[-1]
        name = config.experiment_name+"-"+dirname
        createLink(src=dirpath, dst = os.path.join("/3T/images/",name))
        url = 'http://%s:8080/dataset/%s?page=1&size=50' % (IP, name)
        txt += """ %s <a href='%s'> %s </a></br>""" % (title, url, url)
    vis.text(txt, win='links', env=config.experiment_name)

def save_image(tensor, filename):
    tensor = tensor.cpu()
    ndarr= tensor.mul(255).clamp(0, 255).byte().permute(1, 2, 0).numpy()
    print (ndarr.shape, ndarr.dtype)
    im = Image.fromarray(ndarr)
    im.save(filename)


def padImage(im, out_h, out_w):
    assert(im.width<=out_w)
    assert(im.height<=out_h)
    out = Image.new('RGB', (out_w, out_h), (0, 0, 0)) 
    out.paste(im,(0,0)) 
    return out


def is_url(url):
    return url is not None and urlparse(url).scheme != "" and not os.path.exists(url)

def get_cvmat(path):    
    if is_url(path):
            r = requests.get(path,
                    allow_redirects=False,
                    timeout=2)
            r.raise_for_status()
            stream = cStringIO.StringIO(r.content)
            image = PIL.Image.open(stream)
    else:
        image = PIL.Image.open(path)
    imgcv = np.asarray(image.convert('L'))
    return imgcv


def addGaussRandomNoise(img):
    # add gauss noise
    arr = np.asarray(img)
    r = np.random.randint(0, 2)
    noise = r*np.random.standard_normal(arr.shape[0:2])
    noise = np.dstack((noise,)*arr.shape[2])
    arr = np.clip(arr + noise, 0, 255)
    arr = np.uint8(arr)
    img = Image.fromarray(arr)
    return img


class AverageWithinWindow():
    def __init__(self, win_size):
        self.win_size = win_size
        self.cache = []
        self.average = 0
        self.count = 0 
    def update(self, v):
        if self.count < self.win_size:
            self.cache.append(v);
            self.count += 1
            self.average =  (self.average * (self.count - 1) + v) / self.count
        else:
            idx = self.count  % self.win_size;
            self.average += (v- self.cache[idx]) / self.win_size;
            self.cache[idx] = v;
            self.count += 1


def printGPUINFO():
    gpu_id = config.GPU_ID
    gpu_obj = pynvml.nvmlDeviceGetHandleByIndex(gpu_id)
    print ("gup mem used:", pynvml.nvmlDeviceGetMemoryInfo(gpu_obj).used/1024/1024, "MB")


class MyRandomCrop(object):
    """Crops the given PIL.Image at a random location to have a region of
    the given size. size can be a tuple (target_height, target_width)
    or an integer, in which case the target will be of a square shape (size, size)
    """
    def __init__(self, size, padding=0, stride=1):
        if isinstance(size, numbers.Number):
            self.size = (int(size), int(size))
        else:
            self.size = size
        self.padding = padding
        self.stride = stride

    def __call__(self, img):
        if self.padding > 0:
            img = ImageOps.expand(img, border=self.padding, fill=0)

        w, h = img.size
        th, tw = self.size
        if w == tw and h == th:
            return img

        #x1 = random.randint(0, w - tw)  #[0, w-tw]
        #y1 = random.randint(0, h - th)
        x1 = random.randrange(0, w-tw+1, self.stride)  #[0, w-tw+1)
        y1 = random.randrange(0, h-th+1, self.stride)
        return img.crop((x1, y1, x1 + tw, y1 + th))



def memory_used(model, images):
    print ("before")
    printGPUINFO()
    model.cuda(config.GPU_ID)
    print ("do forward...")
    outputs = model(images.cuda(config.GPU_ID))
    print type(outputs.data)
    print ("after")
    printGPUINFO()
    print (outputs.size())   # (10, 100)
   



