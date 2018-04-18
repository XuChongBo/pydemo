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
import torchvision
import torch.nn as nn
from torch.autograd import Variable
import sys
sys.path.append('..')

from pytorch_ex.model import D
import config

images = Variable(torch.randn(1, 3, config.hr_size, config.hr_size))
d = D.Discriminator()
print "do forward..."
outputs = d(images)
print (outputs.size())   # (10, 100)

def main():
    config.printDetail()
    raw_input("press anykey ")

if __name__ == "__main__":
    main()
