from PIL import Image

file_name='Lenna.png'

# load the image file
lena = Image.open(file_name)
lena.resize((5,5))
print lena.mode
print lena.getpixel((0,0))

lena_ycbcr =lena.convert("YCbCr")
print lena_ycbcr.mode
print lena_ycbcr.getpixel((0,0))


import torch
import torch.nn.functional as F
from torch.autograd import Variable
from torchvision.transforms import ToTensor
rgb = ToTensor()(lena)
rgb = rgb.view(1, rgb.size(0), rgb.size(1), rgb.size(2))
rgb = Variable(rgb)
rgb2ycbcr = Variable(torch.FloatTensor([[0.299, 0.587, 0.114], [-0.169, -0.331, 0.5], [0.5, -0.419, -0.081]]).resize_(3,3,1,1))
print rgb2ycbcr


print "---- rgb -----"
print rgb
ycbcr = F.conv2d(rgb, weight=rgb2ycbcr)

print "first pixel:", rgb.data[0,0,0,0]*255
print lena.getpixel((0,0))

print "---- ycbcr -----"
print ycbcr


print "first pixel:", ycbcr.data[0,0,0,0]*255, (ycbcr.data[0,1,0,0]+0.5)*255
print lena_ycbcr.getpixel((0,0))

ycbcr2rgb = Variable(torch.FloatTensor([[1, -0.00001, 1.402], [1, -0.34413, -0.71414], [1, 1.772, 0.00004]]).resize_(3,3,1,1))
rgb = F.conv2d(ycbcr, weight=ycbcr2rgb)
print "---- rgb -----"
print rgb

print "first pixel:", rgb.data[0,0,0,0]*255
print lena.getpixel((0,0))

def f():
    return 3,4
def g():
    return 5, f()+(6, 8)

print g()
