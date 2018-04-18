import argparse
import os
import shutil
import time
import torch
import torch.nn as nn
import torch.nn.parallel
import torch.backends.cudnn as cudnn
import torch.optim
import torch.utils.data
import torchvision.transforms as transforms
import torch
import random
from PIL import Image
import sys
import os
import dataset 
import utils


train_dataset = dataset.Dataset(desc_file_path='train-data.txt')
train_loader = torch.utils.data.DataLoader(dataset=train_dataset, batch_size=20, shuffle=True, num_workers=1)
save_dir = '/3T/images/eye-inputs'
utils.touchDir(save_dir)
for i, (lr_imgs, hr_imgs) in enumerate(train_loader):
    if i>10:
        break
    print i
    for k in range(lr_imgs.size(0)): 
        utils.save_image(lr_imgs[k], os.path.join(save_dir,'%d_%d.png' %(i, k)) )

