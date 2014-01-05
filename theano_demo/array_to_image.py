#!/usr/bin/env python

import Image
import PIL.Image
import numpy as np
import matplotlib.pyplot as plt

w,h = 512,512
data = np.zeros( (w,h,3), dtype=np.uint8)
data[256,256] = [255,255,0]
#img = PIL.Image.fromarray(data, 'RGB')
img = PIL.Image.fromarray(data)
#print img
img.show()
plt.axis('off')
plt.imshow(img)
img.save('my.png')
