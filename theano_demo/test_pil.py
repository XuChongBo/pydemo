#!/usr/bin/env python

import cPickle
import gzip
import time
import PIL.Image

import numpy
import theano
import theano.tensor as T
import os
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

from theano.tensor.shared_randomstreams import RandomStreams
#from utils import tile_raster_images

working_path='/Users/xcbfreedom/projects/'
os.chdir(working_path)

my_2d_array=numpy.ndarray((5,6,3),dtype='uint8') 
print my_2d_array
image = PIL.Image.fromarray(my_2d_array)
plt.imshow(image)
plt.axis('off')
plt.show()

image.save('./plots/test.png')
